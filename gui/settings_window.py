"""Settings window prototype."""

import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk
from typing import Callable


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.settings import SettingsService  # noqa: E402


SETTINGS_SECTIONS = ("General", "X Export", "YouTube Export", "FFmpeg", "GUI")


def create_settings_window(on_saved: Callable[[], None] | None = None) -> tk.Toplevel:
    """Create the settings prototype window."""
    window = tk.Toplevel()
    window.title("Settings")
    window.geometry("460x720")

    settings_service = SettingsService()
    settings = settings_service.get_settings()
    default_output_folder = tk.StringVar(value=settings.default_output_folder)
    open_output_folder_after_export = tk.BooleanVar(
        value=settings.open_output_folder_after_export
    )
    remember_last_selected_folder = tk.BooleanVar(
        value=settings.remember_last_selected_folder
    )
    encoder = tk.StringVar(value=settings.encoder)
    x_smart_bitrate = tk.BooleanVar(value=settings.x_smart_bitrate)
    x_audio_bitrate = tk.StringVar(value=settings.x_audio_bitrate)
    x_preset = tk.StringVar(value=settings.x_preset)
    x_pixel_format = tk.StringVar(value=settings.x_pixel_format)
    youtube_quality = tk.StringVar(value=settings.youtube_quality)
    youtube_audio_bitrate = tk.StringVar(value=settings.youtube_audio_bitrate)
    youtube_pixel_format = tk.StringVar(value=settings.youtube_pixel_format)
    youtube_faststart = tk.BooleanVar(value=settings.youtube_faststart)
    save_status = tk.StringVar(value="")
    x_save_status = tk.StringVar(value="")
    youtube_save_status = tk.StringVar(value="")

    def choose_output_folder() -> None:
        folder_path = filedialog.askdirectory(
            title="Choose default output folder",
            initialdir=default_output_folder.get() or str(ROOT_DIR),
        )
        if folder_path:
            default_output_folder.set(folder_path)
            remember_last_selected_folder.set(True)

    def save_general_settings() -> None:
        output_folder = default_output_folder.get().strip()
        if not remember_last_selected_folder.get():
            last_selected_folder = ""
        else:
            last_selected_folder = settings.last_selected_folder

        settings_service.update_settings(
            default_output_folder=output_folder,
            last_selected_folder=last_selected_folder,
            remember_last_selected_folder=remember_last_selected_folder.get(),
            open_output_folder_after_export=open_output_folder_after_export.get(),
            encoder=encoder.get(),
        )
        save_status.set("Saved.")
        if on_saved:
            on_saved()

    def save_x_settings() -> None:
        settings_service.update_settings(
            x_smart_bitrate=x_smart_bitrate.get(),
            x_audio_bitrate=x_audio_bitrate.get().strip(),
            x_preset=x_preset.get().strip(),
            x_pixel_format=x_pixel_format.get().strip(),
        )
        x_save_status.set("Saved.")
        if on_saved:
            on_saved()

    def save_youtube_settings() -> None:
        settings_service.update_settings(
            youtube_quality=youtube_quality.get().strip(),
            youtube_audio_bitrate=youtube_audio_bitrate.get().strip(),
            youtube_pixel_format=youtube_pixel_format.get().strip(),
            youtube_faststart=youtube_faststart.get(),
        )
        youtube_save_status.set("Saved.")
        if on_saved:
            on_saved()

    title = tk.Label(window, text="Settings", font=("Segoe UI", 16, "bold"))
    title.pack(pady=(20, 12))

    for section_name in SETTINGS_SECTIONS:
        section_label = tk.Label(window, text=section_name, font=("Segoe UI", 11, "bold"))
        section_label.pack(anchor=tk.W, padx=36, pady=(8, 4))

        if section_name == "General":
            general_frame = tk.Frame(window)
            general_frame.pack(fill=tk.X, padx=36, pady=(0, 8))

            output_label = tk.Label(general_frame, text="Default output folder")
            output_label.pack(anchor=tk.W)

            output_entry = tk.Entry(general_frame, textvariable=default_output_folder)
            output_entry.pack(fill=tk.X, pady=(4, 6))

            browse_button = tk.Button(
                general_frame,
                text="Browse",
                width=12,
                command=choose_output_folder,
            )
            browse_button.pack(anchor=tk.W, pady=(0, 8))

            open_folder_checkbox = tk.Checkbutton(
                general_frame,
                text="Open output folder after export",
                variable=open_output_folder_after_export,
            )
            open_folder_checkbox.pack(anchor=tk.W)

            remember_folder_checkbox = tk.Checkbutton(
                general_frame,
                text="Remember last selected folder",
                variable=remember_last_selected_folder,
            )
            remember_folder_checkbox.pack(anchor=tk.W)

            encoder_label = tk.Label(general_frame, text="Encoder")
            encoder_label.pack(anchor=tk.W, pady=(8, 0))

            encoder_combo = ttk.Combobox(
                general_frame,
                textvariable=encoder,
                values=(
                    "Auto (Recommended)",
                    "NVIDIA NVENC",
                    "Software (libx264)",
                ),
                state="readonly",
            )
            encoder_combo.pack(fill=tk.X, pady=(4, 6))

            save_button = tk.Button(
                general_frame,
                text="Save General Settings",
                command=save_general_settings,
            )
            save_button.pack(anchor=tk.W, pady=(8, 0))

            save_status_label = tk.Label(general_frame, textvariable=save_status)
            save_status_label.pack(anchor=tk.W, pady=(4, 0))

        if section_name == "X Export":
            x_frame = tk.Frame(window)
            x_frame.pack(fill=tk.X, padx=36, pady=(0, 8))

            smart_bitrate_checkbox = tk.Checkbutton(
                x_frame,
                text="Smart Bitrate",
                variable=x_smart_bitrate,
            )
            smart_bitrate_checkbox.pack(anchor=tk.W)

            x_audio_label = tk.Label(x_frame, text="Audio Bitrate")
            x_audio_label.pack(anchor=tk.W, pady=(8, 0))

            x_audio_entry = tk.Entry(x_frame, textvariable=x_audio_bitrate)
            x_audio_entry.pack(fill=tk.X, pady=(4, 6))

            x_preset_label = tk.Label(x_frame, text="Preset")
            x_preset_label.pack(anchor=tk.W)

            x_preset_entry = tk.Entry(x_frame, textvariable=x_preset)
            x_preset_entry.pack(fill=tk.X, pady=(4, 6))

            x_pixel_format_label = tk.Label(x_frame, text="Pixel Format")
            x_pixel_format_label.pack(anchor=tk.W)

            x_pixel_format_entry = tk.Entry(x_frame, textvariable=x_pixel_format)
            x_pixel_format_entry.pack(fill=tk.X, pady=(4, 6))

            x_save_button = tk.Button(
                x_frame,
                text="Save X Export Settings",
                command=save_x_settings,
            )
            x_save_button.pack(anchor=tk.W, pady=(4, 0))

            x_save_status_label = tk.Label(x_frame, textvariable=x_save_status)
            x_save_status_label.pack(anchor=tk.W, pady=(4, 0))

        if section_name == "YouTube Export":
            youtube_frame = tk.Frame(window)
            youtube_frame.pack(fill=tk.X, padx=36, pady=(0, 8))

            youtube_quality_label = tk.Label(youtube_frame, text="Quality")
            youtube_quality_label.pack(anchor=tk.W)

            youtube_quality_entry = tk.Entry(
                youtube_frame,
                textvariable=youtube_quality,
            )
            youtube_quality_entry.pack(fill=tk.X, pady=(4, 6))

            youtube_audio_label = tk.Label(youtube_frame, text="Audio Bitrate")
            youtube_audio_label.pack(anchor=tk.W)

            youtube_audio_entry = tk.Entry(
                youtube_frame,
                textvariable=youtube_audio_bitrate,
            )
            youtube_audio_entry.pack(fill=tk.X, pady=(4, 6))

            youtube_pixel_format_label = tk.Label(
                youtube_frame,
                text="Pixel Format",
            )
            youtube_pixel_format_label.pack(anchor=tk.W)

            youtube_pixel_format_entry = tk.Entry(
                youtube_frame,
                textvariable=youtube_pixel_format,
            )
            youtube_pixel_format_entry.pack(fill=tk.X, pady=(4, 6))

            youtube_faststart_checkbox = tk.Checkbutton(
                youtube_frame,
                text="Faststart",
                variable=youtube_faststart,
            )
            youtube_faststart_checkbox.pack(anchor=tk.W)

            youtube_save_button = tk.Button(
                youtube_frame,
                text="Save YouTube Export Settings",
                command=save_youtube_settings,
            )
            youtube_save_button.pack(anchor=tk.W, pady=(8, 0))

            youtube_save_status_label = tk.Label(
                youtube_frame,
                textvariable=youtube_save_status,
            )
            youtube_save_status_label.pack(anchor=tk.W, pady=(4, 0))

        separator = ttk.Separator(window, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, padx=36)

    return window


def main() -> None:
    root = tk.Tk()
    root.withdraw()
    create_settings_window()
    root.mainloop()


if __name__ == "__main__":
    main()
