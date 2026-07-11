"""Selected media UI component for Exile Creator Kit."""

import tkinter as tk

from gui.components.theme import (
    BACKGROUND,
    BUTTON_ACCENT_BACKGROUND,
    BUTTON_ACCENT_BACKGROUND_HOVER,
    BUTTON_ACCENT_TEXT,
    CARD_BACKGROUND,
    CARD_BORDER,
    CARD_PADDING_X,
    DROP_BORDER,
    FONT_BODY,
    FONT_HEADING,
    FONT_SMALL,
    SHADOW,
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
        pady=7,
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
    outer_frame.pack(fill=tk.X, padx=14, pady=5)

    shadow_frame = tk.Frame(outer_frame, bg=SHADOW)
    shadow_frame.pack(fill=tk.X, padx=(2, 0), pady=(2, 0))

    frame = tk.Frame(
        shadow_frame,
        bg=CARD_BACKGROUND,
        highlightbackground=CARD_BORDER,
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
    selected_video_heading.pack(anchor=tk.W, padx=CARD_PADDING_X, pady=(10, 5))

    drop_area = tk.Canvas(
        frame,
        bg=BACKGROUND,
        height=50,
        borderwidth=0,
        highlightthickness=0,
    )
    drop_area.pack(fill=tk.X, padx=CARD_PADDING_X, pady=(0, 6))
    register_drop_target(drop_area)

    def redraw_drop_area(_event=None) -> None:
        drop_area.delete("all")
        width = max(drop_area.winfo_width(), 1)
        height = max(drop_area.winfo_height(), 1)
        drop_area.create_rectangle(
            2,
            2,
            width - 3,
            height - 3,
            outline=DROP_BORDER,
            dash=(6, 4),
            width=1,
        )
        drop_area.create_text(
            width / 2,
            height / 2 - 10,
            text="↓",
            fill=TEXT_SECONDARY,
            font=(FONT_HEADING[0], 12, "normal"),
        )
        drop_area.create_text(
            width / 2,
            height / 2 + 12,
            text=selected_file_name.get(),
            fill=TEXT_SECONDARY,
            font=FONT_BODY,
        )

    drop_area.bind("<Configure>", redraw_drop_area)
    selected_file_name.trace_add("write", lambda *_args: redraw_drop_area())

    media_info_label = tk.Label(
        frame,
        textvariable=media_info_text,
        justify=tk.LEFT,
        bg=CARD_BACKGROUND,
        fg=TEXT_SECONDARY,
        font=FONT_SMALL,
    )
    media_info_label.pack(anchor=tk.W, padx=CARD_PADDING_X, pady=(0, 5))

    choose_button = tk.Button(
        frame,
        text="□  Choose Video",
        width=22,
        command=on_choose_video,
    )
    _style_accent_button(choose_button)
    choose_button.pack(pady=(0, 10))

    return outer_frame
