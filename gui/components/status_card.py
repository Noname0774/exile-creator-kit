"""Export status UI component for Exile Creator Kit."""

import tkinter as tk
from tkinter import ttk

from gui.components.theme import (
    ACCENT_RED,
    BACKGROUND,
    BORDER,
    BUTTON_BACKGROUND,
    BUTTON_BACKGROUND_HOVER,
    BUTTON_DISABLED_TEXT,
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


def _attach_hover(button: tk.Button) -> None:
    def on_enter(_event) -> None:
        if button["state"] == tk.NORMAL:
            button.configure(bg=BUTTON_BACKGROUND_HOVER)

    def on_leave(_event) -> None:
        if button["state"] == tk.NORMAL:
            button.configure(bg=BUTTON_BACKGROUND)

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)


def _style_button(button: tk.Button) -> None:
    button.configure(
        bg=BUTTON_BACKGROUND,
        fg=BUTTON_TEXT,
        activebackground=BUTTON_BACKGROUND_HOVER,
        activeforeground=BUTTON_TEXT,
        disabledforeground=BUTTON_DISABLED_TEXT,
        relief=tk.FLAT,
        borderwidth=1,
        highlightbackground=BORDER,
        highlightcolor=BORDER,
        highlightthickness=1,
        font=FONT_BODY,
        cursor="hand2",
        pady=5,
    )
    _attach_hover(button)


def build_status_card(
    parent: tk.Widget,
    *,
    export_status: tk.StringVar,
    export_message: tk.StringVar,
    on_open_output_folder,
    on_open_log_folder,
) -> dict[str, tk.Widget]:
    """Build the export status area."""
    outer_frame = tk.Frame(parent, bg=BACKGROUND)
    outer_frame.pack(fill=tk.BOTH, expand=True, padx=(8, 14), pady=5)

    shadow_frame = tk.Frame(outer_frame, bg=SHADOW)
    shadow_frame.pack(fill=tk.BOTH, expand=True, padx=(2, 0), pady=(2, 0))

    frame = tk.Frame(
        shadow_frame,
        bg=CARD_BACKGROUND,
        highlightbackground=CARD_BORDER,
        highlightthickness=1,
        borderwidth=0,
        height=CARD_MIN_HEIGHT,
    )
    frame.pack(fill=tk.BOTH, expand=True, padx=(0, 2), pady=(0, 2))
    frame.pack_propagate(False)

    status_heading = tk.Label(
        frame,
        text="Status",
        bg=CARD_BACKGROUND,
        fg=TEXT_PRIMARY,
        font=FONT_HEADING,
    )
    status_heading.pack(anchor=tk.W, padx=CARD_PADDING_X, pady=(14, 4))

    status_label = tk.Label(
        frame,
        textvariable=export_status,
        bg=CARD_BACKGROUND,
        fg=ACCENT_RED,
        font=FONT_BODY,
    )
    status_label.pack(anchor=tk.W, padx=CARD_PADDING_X, pady=(0, 6))

    style = ttk.Style(frame)
    style.configure(
        "ECK.Horizontal.TProgressbar",
        background=ACCENT_RED,
        troughcolor=BACKGROUND,
        bordercolor=BORDER,
        lightcolor=ACCENT_RED,
        darkcolor=ACCENT_RED,
        thickness=9,
    )
    progress_bar = ttk.Progressbar(
        frame,
        mode="indeterminate",
        length=300,
        style="ECK.Horizontal.TProgressbar",
    )
    progress_bar.pack(fill=tk.X, padx=CARD_PADDING_X)

    message_label = tk.Label(
        frame,
        textvariable=export_message,
        bg=CARD_BACKGROUND,
        fg=TEXT_SECONDARY,
        font=FONT_SMALL,
        justify=tk.LEFT,
        wraplength=260,
    )
    message_label.pack(anchor=tk.W, padx=CARD_PADDING_X, pady=(8, 0))

    button_row = tk.Frame(frame, bg=CARD_BACKGROUND)
    button_row.pack(side=tk.BOTTOM, pady=(8, 14))

    open_output_button = tk.Button(
        button_row,
        text="□  Open Output Folder",
        width=19,
        state=tk.DISABLED,
        command=on_open_output_folder,
    )
    _style_button(open_output_button)
    open_output_button.pack(side=tk.LEFT, padx=(0, 6))

    open_log_button = tk.Button(
        button_row,
        text="▤  Open Log Folder",
        width=19,
        state=tk.DISABLED,
        command=on_open_log_folder,
    )
    _style_button(open_log_button)
    open_log_button.pack(side=tk.LEFT, padx=(6, 0))

    return {
        "progress_bar": progress_bar,
        "open_output_button": open_output_button,
        "open_log_button": open_log_button,
    }
