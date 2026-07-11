"""Export action UI component for Exile Creator Kit."""

import tkinter as tk

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
    FONT_BODY,
    FONT_HEADING,
    FONT_SMALL,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


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
    outer_frame.pack(fill=tk.X, padx=12, pady=4)

    shadow_frame = tk.Frame(outer_frame, bg="#050608")
    shadow_frame.pack(fill=tk.X, padx=(3, 0), pady=(3, 0))

    button_frame = tk.Frame(
        shadow_frame,
        bg=CARD_BACKGROUND,
        highlightbackground=ACCENT_RED,
        highlightthickness=1,
        borderwidth=0,
    )
    button_frame.pack(fill=tk.X, padx=(0, 3), pady=(0, 3))

    export_heading = tk.Label(
        button_frame,
        text="Export",
        bg=CARD_BACKGROUND,
        fg=TEXT_PRIMARY,
        font=(FONT_HEADING[0], 11, FONT_HEADING[2]),
    )
    export_heading.pack(anchor=tk.W, padx=24, pady=(10, 2))

    export_description = tk.Label(
        button_frame,
        text="Choose the upload target.",
        bg=CARD_BACKGROUND,
        fg=TEXT_SECONDARY,
        font=FONT_SMALL,
    )
    export_description.pack(anchor=tk.W, padx=24, pady=(0, 7))

    preset_label = tk.Label(
        button_frame,
        text="Export Preset",
        bg=CARD_BACKGROUND,
        fg=TEXT_SECONDARY,
        font=FONT_SMALL,
    )
    preset_label.pack(anchor=tk.W, padx=24, pady=(0, 4))

    preset_selector = tk.OptionMenu(
        button_frame,
        selected_preset,
        *preset_names,
        command=on_preset_selected,
    )
    _style_option_menu(preset_selector)
    preset_selector.pack(fill=tk.X, padx=24, pady=(0, 6))

    current_preset_label = tk.Label(
        button_frame,
        textvariable=selected_preset,
        bg=CARD_BACKGROUND,
        fg=TEXT_PRIMARY,
        font=FONT_BODY,
        wraplength=320,
        justify=tk.LEFT,
    )
    current_preset_label.pack(anchor=tk.W, padx=24, pady=(0, 3))

    preset_description_label = tk.Label(
        button_frame,
        textvariable=preset_description,
        bg=CARD_BACKGROUND,
        fg=TEXT_SECONDARY,
        font=FONT_SMALL,
        wraplength=320,
        justify=tk.LEFT,
    )
    preset_description_label.pack(anchor=tk.W, padx=24, pady=(0, 6))

    encoder_label = tk.Label(
        button_frame,
        textvariable=recommended_encoder,
        bg=CARD_BACKGROUND,
        fg=TEXT_SECONDARY,
        font=FONT_SMALL,
        wraplength=320,
        justify=tk.LEFT,
    )
    encoder_label.pack(anchor=tk.W, padx=24, pady=(0, 10))

    x_button = tk.Button(
        button_frame,
        text="Export for X (512 MB)",
        width=36,
        command=on_export_x,
    )
    _style_button(x_button, accent=True)
    x_button.pack(pady=(0, 7))

    youtube_button = tk.Button(
        button_frame,
        text="Export for YouTube (High Quality)",
        width=36,
        command=on_export_youtube,
    )
    _style_button(youtube_button)
    youtube_button.pack(pady=(0, 10))

    return {
        "preset_selector": preset_selector,
        "x_button": x_button,
        "youtube_button": youtube_button,
    }
