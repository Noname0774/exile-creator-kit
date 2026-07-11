"""Header UI component for Exile Creator Kit."""

import tkinter as tk
from pathlib import Path
from tkinter import ttk

from PIL import Image, ImageTk

from gui.components.theme import (
    ACCENT_RED,
    BACKGROUND,
    BORDER,
    BUTTON_BACKGROUND,
    BUTTON_BACKGROUND_HOVER,
    BUTTON_TEXT,
    FONT_BODY,
    FONT_SMALL,
    FONT_TITLE,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


def _attach_hover(button: tk.Button) -> None:
    button.bind("<Enter>", lambda _event: button.configure(bg=BUTTON_BACKGROUND_HOVER))
    button.bind("<Leave>", lambda _event: button.configure(bg=BUTTON_BACKGROUND))


def _style_button(button: tk.Button) -> None:
    button.configure(
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
        pady=4,
    )
    _attach_hover(button)


def build_header(
    parent: tk.Widget,
    *,
    logo_file: Path,
    on_settings,
    on_about,
) -> tk.Frame:
    """Build the application header."""
    parent.configure(bg=BACKGROUND)
    ttk.Style(parent).configure("TSeparator", background=BORDER)

    frame = tk.Frame(parent, bg=BACKGROUND)
    frame.pack(fill=tk.X, padx=18, pady=(4, 2))

    if logo_file.exists():
        logo_image = Image.open(logo_file)
        logo_image = logo_image.resize((76, 76), Image.Resampling.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)

        logo_label = tk.Label(frame, image=logo_photo, bg=BACKGROUND, borderwidth=0)
        logo_label.image = logo_photo
        logo_label.pack(pady=(0, 3))
    else:
        logo_label = tk.Label(
            frame,
            text="ECK",
            bg=BACKGROUND,
            fg=ACCENT_RED,
            font=("Segoe UI Semibold", 22, "normal"),
        )
        logo_label.pack(pady=(0, 2))

    title = tk.Label(
        frame,
        text="Exile Creator Kit",
        bg=BACKGROUND,
        fg=TEXT_PRIMARY,
        font=(FONT_TITLE[0], 19, FONT_TITLE[2]),
    )
    title.pack(pady=(0, 1))

    accent_line = tk.Frame(frame, bg=ACCENT_RED, width=108, height=2)
    accent_line.pack(pady=(0, 3))

    description = tk.Label(
        frame,
        text="Create upload-ready videos for X and YouTube",
        bg=BACKGROUND,
        fg=TEXT_SECONDARY,
        font=FONT_SMALL,
        wraplength=360,
    )
    description.pack()

    app_button_frame = tk.Frame(frame, bg=BACKGROUND)
    app_button_frame.pack(pady=(7, 0))

    settings_button = tk.Button(
        app_button_frame,
        text="Settings",
        width=14,
        command=on_settings,
    )
    _style_button(settings_button)
    settings_button.pack(side=tk.LEFT, padx=4)

    about_button = tk.Button(
        app_button_frame,
        text="About",
        width=14,
        command=on_about,
    )
    _style_button(about_button)
    about_button.pack(side=tk.LEFT, padx=4)

    return frame
