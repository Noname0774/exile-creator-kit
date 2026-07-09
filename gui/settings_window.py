"""Settings window prototype."""

import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.settings import SettingsService  # noqa: E402


SETTINGS_SECTIONS = ("General", "X Export", "YouTube Export", "FFmpeg", "GUI")


def create_settings_window() -> tk.Toplevel:
    """Create the settings prototype window."""
    window = tk.Toplevel()
    window.title("Settings")
    window.geometry("420x420")

    settings_service = SettingsService()
    settings = settings_service.get_settings()
    default_output_folder = tk.StringVar(value=settings.default_output_folder)
    open_output_folder_after_export = tk.BooleanVar(
        value=settings.open_output_folder_after_export
    )
    remember_last_selected_folder = tk.BooleanVar(
        value=bool(settings.default_output_folder)
    )
    save_status = tk.StringVar(value="")

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
            output_folder = ""

        settings_service.update_settings(
            default_output_folder=output_folder,
            open_output_folder_after_export=open_output_folder_after_export.get(),
        )
        save_status.set("Saved.")

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

            save_button = tk.Button(
                general_frame,
                text="Save General Settings",
                command=save_general_settings,
            )
            save_button.pack(anchor=tk.W, pady=(8, 0))

            save_status_label = tk.Label(general_frame, textvariable=save_status)
            save_status_label.pack(anchor=tk.W, pady=(4, 0))

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
