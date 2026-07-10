"""Header UI component for Exile Creator Kit."""

import tkinter as tk
from pathlib import Path

from PIL import Image, ImageTk


def build_header(
    parent: tk.Widget,
    *,
    logo_file: Path,
    on_settings,
    on_about,
) -> tk.Frame:
    """Build the application header."""
    frame = tk.Frame(parent)
    frame.pack()

    if logo_file.exists():
        logo_image = Image.open(logo_file)
        logo_image = logo_image.resize((96, 96), Image.Resampling.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)

        logo_label = tk.Label(frame, image=logo_photo)
        logo_label.image = logo_photo
        logo_label.pack(pady=(10, 5))

    title = tk.Label(frame, text="Exile Creator Kit", font=("Segoe UI", 18, "bold"))
    title.pack(pady=(8, 6))

    description = tk.Label(
        frame,
        text="Create upload-ready videos for X and YouTube",
    )
    description.pack()

    app_button_frame = tk.Frame(frame)
    app_button_frame.pack(pady=(10, 0))

    settings_button = tk.Button(
        app_button_frame,
        text="Settings",
        width=16,
        command=on_settings,
    )
    settings_button.pack(side=tk.LEFT, padx=4)

    about_button = tk.Button(
        app_button_frame,
        text="About",
        width=16,
        command=on_about,
    )
    about_button.pack(side=tk.LEFT, padx=4)

    return frame
