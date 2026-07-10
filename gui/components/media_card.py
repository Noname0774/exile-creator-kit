"""Selected media UI component for Exile Creator Kit."""

import tkinter as tk

from gui.components.theme import (
    ACCENT_RED,
    BACKGROUND,
    BORDER,
    BUTTON_ACCENT_BACKGROUND,
    BUTTON_ACCENT_BACKGROUND_HOVER,
    BUTTON_ACCENT_TEXT,
    CARD_BACKGROUND,
    FONT_BODY,
    FONT_HEADING,
    FONT_SMALL,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


def _attach_accent_hover(button: tk.Button) -> None:
    button.bind(
        "<Enter>",
        lambda _event: button.configure(bg=BUTTON_ACCENT_BACKGROUND_HOVER),
    )
    button.bind(
        "<Leave>",
        lambda _event: button.configure(bg=BUTTON_ACCENT_BACKGROUND),
    )


def _style_accent_button(button: tk.Button) -> None:
    button.configure(
        bg=BUTTON_ACCENT_BACKGROUND,
        fg=BUTTON_ACCENT_TEXT,
        activebackground=BUTTON_ACCENT_BACKGROUND_HOVER,
        activeforeground=BUTTON_ACCENT_TEXT,
        relief=tk.FLAT,
        borderwidth=0,
        highlightthickness=0,
        font=FONT_BODY,
        cursor="hand2",
        pady=9,
    )
    _attach_accent_hover(button)


def build_media_card(
    parent: tk.Widget,
    *,
    selected_file_name: tk.StringVar,
    media_info_text: tk.StringVar,
    on_choose_video,
    register_drop_target,
) -> tk.Frame:
    """Build the selected video area."""
    outer_frame = tk.Frame(parent, bg=BACKGROUND)
    outer_frame.pack(fill=tk.X, padx=14, pady=4)

    shadow_frame = tk.Frame(outer_frame, bg="#050608")
    shadow_frame.pack(fill=tk.X, padx=(2, 0), pady=(2, 0))

    frame = tk.Frame(
        shadow_frame,
        bg=CARD_BACKGROUND,
        highlightbackground=BORDER,
        highlightthickness=1,
        borderwidth=0,
    )
    frame.pack(fill=tk.X, padx=(0, 2), pady=(0, 2))

    selected_video_heading = tk.Label(
        frame,
        text="Selected Video",
        bg=CARD_BACKGROUND,
        fg=TEXT_PRIMARY,
        font=FONT_HEADING,
    )
    selected_video_heading.pack(anchor=tk.W, padx=24, pady=(12, 6))

    drop_area = tk.Label(
        frame,
        textvariable=selected_file_name,
        bg=BACKGROUND,
        fg=TEXT_SECONDARY,
        activebackground=BACKGROUND,
        relief=tk.FLAT,
        highlightbackground=ACCENT_RED,
        highlightthickness=1,
        font=FONT_BODY,
        width=28,
        height=1,
    )
    drop_area.pack(fill=tk.X, padx=24, pady=(0, 8))
    register_drop_target(drop_area)

    media_info_label = tk.Label(
        frame,
        textvariable=media_info_text,
        justify=tk.LEFT,
        bg=CARD_BACKGROUND,
        fg=TEXT_SECONDARY,
        font=FONT_SMALL,
    )
    media_info_label.pack(anchor=tk.W, padx=24, pady=(0, 8))

    choose_button = tk.Button(
        frame,
        text="Choose Video",
        width=22,
        command=on_choose_video,
    )
    _style_accent_button(choose_button)
    choose_button.pack(pady=(0, 12))

    return outer_frame
