"""Settings window for Exile Creator Kit."""

import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk
from typing import Callable


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.export.presets import PresetRepository  # noqa: E402
from core.settings import SettingsService  # noqa: E402
from core.system import EncoderSelector, EnvironmentDetector  # noqa: E402
from gui.components.theme import (  # noqa: E402
    ACCENT_RED,
    BACKGROUND,
    BORDER,
    BUTTON_ACCENT_BACKGROUND,
    BUTTON_ACCENT_BACKGROUND_HOVER,
    BUTTON_ACCENT_TEXT,
    BUTTON_BACKGROUND,
    BUTTON_BACKGROUND_HOVER,
    BUTTON_TEXT,
    CARD_BACKGROUND,
    FONT_BODY,
    FONT_HEADING,
    FONT_SMALL,
    FONT_TITLE,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


ENCODER_OPTIONS = (
    "Auto (Recommended)",
    "NVIDIA NVENC",
    "Software (libx264)",
)


def _style_button(button: tk.Button, *, accent: bool = False) -> None:
    normal = BUTTON_ACCENT_BACKGROUND if accent else BUTTON_BACKGROUND
    hover = BUTTON_ACCENT_BACKGROUND_HOVER if accent else BUTTON_BACKGROUND_HOVER
    text = BUTTON_ACCENT_TEXT if accent else BUTTON_TEXT
    button.configure(
        bg=normal,
        fg=text,
        activebackground=hover,
        activeforeground=text,
        relief=tk.FLAT,
        borderwidth=1,
        highlightbackground=ACCENT_RED if accent else BORDER,
        highlightcolor=ACCENT_RED if accent else BORDER,
        highlightthickness=1,
        font=FONT_BODY,
        cursor="hand2",
        padx=12,
        pady=7,
    )
    button.bind("<Enter>", lambda _event: button.configure(bg=hover))
    button.bind("<Leave>", lambda _event: button.configure(bg=normal))


def _style_entry(entry: tk.Entry) -> None:
    entry.configure(
        bg=BUTTON_BACKGROUND,
        fg=TEXT_PRIMARY,
        insertbackground=TEXT_PRIMARY,
        relief=tk.FLAT,
        borderwidth=1,
        highlightbackground=BORDER,
        highlightcolor=ACCENT_RED,
        highlightthickness=1,
        font=FONT_BODY,
    )


def _style_checkbutton(checkbutton: tk.Checkbutton) -> None:
    checkbutton.configure(
        bg=CARD_BACKGROUND,
        fg=TEXT_SECONDARY,
        activebackground=CARD_BACKGROUND,
        activeforeground=TEXT_PRIMARY,
        selectcolor=BUTTON_BACKGROUND,
        font=FONT_BODY,
    )


def _style_option_menu(option_menu: tk.OptionMenu) -> None:
    option_menu.configure(
        bg=BUTTON_BACKGROUND,
        fg=BUTTON_TEXT,
        activebackground=BUTTON_BACKGROUND_HOVER,
        activeforeground=BUTTON_TEXT,
        relief=tk.FLAT,
        borderwidth=1,
        highlightbackground=BORDER,
        highlightcolor=ACCENT_RED,
        highlightthickness=1,
        font=FONT_BODY,
        cursor="hand2",
    )
    option_menu["menu"].configure(
        bg=CARD_BACKGROUND,
        fg=TEXT_PRIMARY,
        activebackground=BUTTON_BACKGROUND_HOVER,
        activeforeground=BUTTON_TEXT,
        relief=tk.FLAT,
        font=FONT_BODY,
    )


def _card(parent: tk.Widget, title: str, description: str) -> tk.Frame:
    frame = tk.Frame(
        parent,
        bg=CARD_BACKGROUND,
        highlightbackground=BORDER,
        highlightthickness=1,
        borderwidth=0,
    )
    frame.pack(fill=tk.X, padx=24, pady=(0, 14))

    title_label = tk.Label(
        frame,
        text=title,
        bg=CARD_BACKGROUND,
        fg=TEXT_PRIMARY,
        font=FONT_HEADING,
    )
    title_label.pack(anchor=tk.W, padx=22, pady=(16, 2))

    description_label = tk.Label(
        frame,
        text=description,
        bg=CARD_BACKGROUND,
        fg=TEXT_SECONDARY,
        font=FONT_SMALL,
        wraplength=560,
        justify=tk.LEFT,
    )
    description_label.pack(anchor=tk.W, padx=22, pady=(0, 12))
    return frame


def _field_label(parent: tk.Widget, text: str) -> None:
    label = tk.Label(parent, text=text, bg=CARD_BACKGROUND, fg=TEXT_SECONDARY, font=FONT_SMALL)
    label.pack(anchor=tk.W, padx=22, pady=(0, 4))


def _option_menu(
    parent: tk.Widget,
    variable: tk.StringVar,
    values: tuple[str, ...],
) -> tk.OptionMenu:
    option_menu = tk.OptionMenu(parent, variable, *values)
    _style_option_menu(option_menu)
    option_menu.pack(fill=tk.X, padx=22, pady=(0, 10))
    return option_menu


def _short_tool_version(version_text: str) -> str:
    if not version_text or version_text == "Unknown":
        return "Unknown"

    version = version_text.split(" Copyright", 1)[0].strip()
    if len(version) <= 58:
        return version

    return f"{version[:55]}..."


def create_settings_window(on_saved: Callable[[], None] | None = None) -> tk.Toplevel:
    """Create the settings window."""
    window = tk.Toplevel()
    window.title("Settings")
    window.geometry("560x760")
    window.minsize(500, 620)
    window.configure(bg=BACKGROUND)

    style = ttk.Style(window)
    style.configure("Vertical.TScrollbar", background=BUTTON_BACKGROUND)

    settings_service = SettingsService()
    settings = settings_service.get_settings()
    preset_repository = PresetRepository()
    preset_names = preset_repository.list_names()
    environment_info = EnvironmentDetector(settings_service=settings_service).detect()
    encoder_decision = EncoderSelector().select(environment_info)

    default_output_folder = tk.StringVar(value=settings.default_output_folder)
    default_export_preset = tk.StringVar(
        value=settings.default_export_preset
        if settings.default_export_preset in preset_names
        else preset_names[0]
    )
    encoder = tk.StringVar(value=settings.encoder)
    open_output_folder_after_export = tk.BooleanVar(
        value=settings.open_output_folder_after_export
    )
    remember_last_selected_folder = tk.BooleanVar(
        value=settings.remember_last_selected_folder
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

    def save_settings() -> None:
        if not remember_last_selected_folder.get():
            last_selected_folder = ""
        else:
            last_selected_folder = settings_service.get_settings().last_selected_folder

        settings_service.update_settings(
            default_output_folder=default_output_folder.get().strip(),
            default_export_preset=default_export_preset.get(),
            encoder=encoder.get(),
            last_selected_folder=last_selected_folder,
            remember_last_selected_folder=remember_last_selected_folder.get(),
            open_output_folder_after_export=open_output_folder_after_export.get(),
        )
        save_status.set("Saved.")
        if on_saved:
            on_saved()

    canvas = tk.Canvas(window, bg=BACKGROUND, borderwidth=0, highlightthickness=0)
    scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    content_frame = tk.Frame(canvas, bg=BACKGROUND)
    content_window = canvas.create_window((0, 0), window=content_frame, anchor=tk.N)

    def update_scroll_region(_event=None) -> None:
        canvas.configure(scrollregion=canvas.bbox(tk.ALL))

    def resize_content(event) -> None:
        content_width = min(event.width, 520)
        canvas.itemconfigure(content_window, width=content_width)
        canvas.coords(content_window, event.width // 2, 0)

    content_frame.bind("<Configure>", update_scroll_region)
    canvas.bind("<Configure>", resize_content)

    title = tk.Label(
        content_frame,
        text="Settings",
        bg=BACKGROUND,
        fg=TEXT_PRIMARY,
        font=FONT_TITLE,
    )
    title.pack(pady=(24, 4))

    subtitle = tk.Label(
        content_frame,
        text="Configure the creator workflow and environment defaults.",
        bg=BACKGROUND,
        fg=TEXT_SECONDARY,
        font=FONT_BODY,
    )
    subtitle.pack(pady=(0, 18))

    environment_card = _card(
        content_frame,
        "Environment",
        "Detected system information used by Exile Creator Kit.",
    )
    environment_lines = (
        f"GPU: {environment_info.gpu_vendor} - {environment_info.gpu_name}",
        f"Encoder: {encoder_decision.auto_label}",
        f"FFmpeg: {_short_tool_version(environment_info.ffmpeg_version)}",
        f"Version: {environment_info.app_version}",
    )
    environment_label = tk.Label(
        environment_card,
        text="\n".join(environment_lines),
        bg=CARD_BACKGROUND,
        fg=TEXT_PRIMARY,
        font=FONT_BODY,
        justify=tk.LEFT,
        wraplength=470,
    )
    environment_label.pack(anchor=tk.W, padx=22, pady=(0, 16))

    preset_card = _card(
        content_frame,
        "Export Defaults",
        "Choose the preset and encoder behavior used as application defaults.",
    )
    _field_label(preset_card, "Default Export Preset")
    _option_menu(preset_card, default_export_preset, preset_names)

    _field_label(preset_card, "Default Encoder")
    _option_menu(preset_card, encoder, ENCODER_OPTIONS)

    encoder_help = tk.Label(
        preset_card,
        text=(
            "Auto uses the detected encoder first. Manual choices force the selected "
            "encoder behavior."
        ),
        bg=CARD_BACKGROUND,
        fg=TEXT_SECONDARY,
        font=FONT_SMALL,
        wraplength=470,
        justify=tk.LEFT,
    )
    encoder_help.pack(anchor=tk.W, padx=22, pady=(0, 16))

    output_card = _card(
        content_frame,
        "Output Folder",
        "Control where exports are saved and how folders behave after export.",
    )
    _field_label(output_card, "Default Output Folder")
    output_entry = tk.Entry(output_card, textvariable=default_output_folder)
    _style_entry(output_entry)
    output_entry.pack(fill=tk.X, padx=22, pady=(0, 8), ipady=5)

    browse_button = tk.Button(output_card, text="Browse", width=14, command=choose_output_folder)
    _style_button(browse_button)
    browse_button.pack(anchor=tk.W, padx=22, pady=(0, 12))

    open_folder_checkbox = tk.Checkbutton(
        output_card,
        text="Open output folder after export",
        variable=open_output_folder_after_export,
    )
    _style_checkbutton(open_folder_checkbox)
    open_folder_checkbox.pack(anchor=tk.W, padx=18, pady=(0, 4))

    remember_folder_checkbox = tk.Checkbutton(
        output_card,
        text="Remember last selected folder",
        variable=remember_last_selected_folder,
    )
    _style_checkbutton(remember_folder_checkbox)
    remember_folder_checkbox.pack(anchor=tk.W, padx=18, pady=(0, 16))

    save_button = tk.Button(content_frame, text="Save Settings", command=save_settings)
    _style_button(save_button, accent=True)
    save_button.pack(pady=(2, 8))

    save_status_label = tk.Label(
        content_frame,
        textvariable=save_status,
        bg=BACKGROUND,
        fg=TEXT_SECONDARY,
        font=FONT_BODY,
    )
    save_status_label.pack(pady=(0, 24))

    return window


def main() -> None:
    root = tk.Tk()
    root.withdraw()
    create_settings_window()
    root.mainloop()


if __name__ == "__main__":
    main()
