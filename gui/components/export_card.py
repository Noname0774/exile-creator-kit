"""Export action UI component for Exile Creator Kit."""

import tkinter as tk
from pathlib import Path

from PIL import Image, ImageTk

from gui.components.theme import (
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
    CARD_BORDER,
    CARD_MIN_HEIGHT,
    CARD_PADDING_X,
    FONT_BODY,
    FONT_HEADING,
    FONT_SMALL,
    SHADOW,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)

ROOT_DIR = Path(__file__).resolve().parents[2]
ICON_SIZE = (26, 26)


def _attach_hover(button: tk.Button, *, accent: bool = False) -> None:
    normal = BUTTON_ACCENT_BACKGROUND if accent else BUTTON_BACKGROUND
    hover = BUTTON_ACCENT_BACKGROUND_HOVER if accent else BUTTON_BACKGROUND_HOVER
    button.bind("<Enter>", lambda _event: button.configure(bg=hover))
    button.bind("<Leave>", lambda _event: button.configure(bg=normal))


def _style_button(button: tk.Button, *, accent: bool = False) -> None:
    button.configure(
        bg=BUTTON_ACCENT_BACKGROUND if accent else BUTTON_BACKGROUND,
        fg=BUTTON_ACCENT_TEXT if accent else BUTTON_TEXT,
        activebackground=BUTTON_ACCENT_BACKGROUND_HOVER
        if accent
        else BUTTON_BACKGROUND_HOVER,
        activeforeground=BUTTON_ACCENT_TEXT if accent else BUTTON_TEXT,
        relief=tk.FLAT,
        borderwidth=1,
        highlightbackground=ACCENT_RED if accent else BORDER,
        highlightcolor=ACCENT_RED if accent else BORDER,
        highlightthickness=1,
        font=(FONT_HEADING[0] if accent else FONT_BODY[0], 10, "normal"),
        cursor="hand2",
        pady=8 if accent else 7,
    )
    _attach_hover(button, accent=accent)


def _load_icon(file_name: str) -> ImageTk.PhotoImage | None:
    icon_path = ROOT_DIR / "assets" / "icons" / file_name
    if not icon_path.exists():
        return None

    try:
        icon = Image.open(icon_path).convert("RGBA")
        icon.thumbnail(ICON_SIZE, Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", ICON_SIZE, (0, 0, 0, 0))
        x = (ICON_SIZE[0] - icon.width) // 2
        y = (ICON_SIZE[1] - icon.height) // 2
        canvas.alpha_composite(icon, (x, y))
        return ImageTk.PhotoImage(canvas)
    except OSError:
        return None


def _apply_button_icon(button: tk.Button, file_name: str) -> None:
    icon = _load_icon(file_name)
    if icon is None:
        return

    button.configure(image=icon, compound=tk.LEFT, padx=14)
    button.image = icon


def _style_option_menu(option_menu: tk.OptionMenu) -> None:
    option_menu.configure(
        bg=BUTTON_BACKGROUND,
        fg=BUTTON_TEXT,
        activebackground=BUTTON_BACKGROUND_HOVER,
        activeforeground=BUTTON_TEXT,
        relief=tk.FLAT,
        borderwidth=1,
        highlightbackground=BORDER,
        highlightcolor=BORDER,
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


def build_export_card(
    parent: tk.Widget,
    *,
    preset_names: tuple[str, ...],
    selected_preset: tk.StringVar,
    preset_description: tk.StringVar,
    recommended_encoder: tk.StringVar,
    on_preset_selected,
    on_export_x,
    on_export_youtube,
) -> dict[str, tk.Widget]:
    """Build the export action area."""
    outer_frame = tk.Frame(parent, bg=BACKGROUND)
    outer_frame.pack(fill=tk.BOTH, expand=True, padx=(14, 8), pady=5)

    shadow_frame = tk.Frame(outer_frame, bg=SHADOW)
    shadow_frame.pack(fill=tk.BOTH, expand=True, padx=(2, 0), pady=(2, 0))

    button_frame = tk.Frame(
        shadow_frame,
        bg=CARD_BACKGROUND,
        highlightbackground=CARD_BORDER,
        highlightthickness=1,
        borderwidth=0,
        height=CARD_MIN_HEIGHT,
    )
    button_frame.pack(fill=tk.BOTH, expand=True, padx=(0, 2), pady=(0, 2))
    button_frame.pack_propagate(False)

    export_heading = tk.Label(
        button_frame,
        text="Export",
        bg=CARD_BACKGROUND,
        fg=TEXT_PRIMARY,
        font=(FONT_HEADING[0], 11, FONT_HEADING[2]),
    )
    export_heading.pack(anchor=tk.W, padx=CARD_PADDING_X, pady=(14, 2))

    export_description = tk.Label(
        button_frame,
        text="Choose the upload target.",
        bg=CARD_BACKGROUND,
        fg=TEXT_SECONDARY,
        font=FONT_SMALL,
    )
    export_description.pack(anchor=tk.W, padx=CARD_PADDING_X, pady=(0, 7))

    x_button = tk.Button(
        button_frame,
        text="Export for X (512 MB)",
        width=38,
        command=on_export_x,
    )
    _style_button(x_button, accent=True)
    _apply_button_icon(x_button, "x-logo.png")
    x_button.pack(fill=tk.X, padx=CARD_PADDING_X, pady=(0, 8))

    youtube_button = tk.Button(
        button_frame,
        text="Export for YouTube (High Quality)",
        width=38,
        command=on_export_youtube,
    )
    _style_button(youtube_button)
    _apply_button_icon(youtube_button, "youtube-logo.png")
    youtube_button.pack(fill=tk.X, padx=CARD_PADDING_X, pady=(0, 12))

    preset_label = tk.Label(
        button_frame,
        text="Export Preset",
        bg=CARD_BACKGROUND,
        fg=TEXT_SECONDARY,
        font=FONT_SMALL,
    )
    preset_label.pack(anchor=tk.W, padx=CARD_PADDING_X, pady=(0, 4))

    preset_selector = tk.OptionMenu(
        button_frame,
        selected_preset,
        *preset_names,
        command=on_preset_selected,
    )
    _style_option_menu(preset_selector)
    preset_selector.pack(fill=tk.X, padx=CARD_PADDING_X, pady=(0, 6))

    current_preset_label = tk.Label(
        button_frame,
        textvariable=selected_preset,
        bg=CARD_BACKGROUND,
        fg=TEXT_PRIMARY,
        font=FONT_BODY,
        wraplength=320,
        justify=tk.LEFT,
    )
    current_preset_label.pack(anchor=tk.W, padx=CARD_PADDING_X, pady=(0, 3))

    preset_description_label = tk.Label(
        button_frame,
        textvariable=preset_description,
        bg=CARD_BACKGROUND,
        fg=TEXT_SECONDARY,
        font=FONT_SMALL,
        wraplength=320,
        justify=tk.LEFT,
    )
    preset_description_label.pack(anchor=tk.W, padx=CARD_PADDING_X, pady=(0, 6))

    encoder_label = tk.Label(
        button_frame,
        textvariable=recommended_encoder,
        bg=CARD_BACKGROUND,
        fg=TEXT_SECONDARY,
        font=FONT_SMALL,
        wraplength=320,
        justify=tk.LEFT,
    )
    encoder_label.pack(anchor=tk.W, padx=CARD_PADDING_X, pady=(0, 10))

    return {
        "preset_selector": preset_selector,
        "x_button": x_button,
        "youtube_button": youtube_button,
    }
