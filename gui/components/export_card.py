"""Export action UI component for Exile Creator Kit."""

import tkinter as tk


def build_export_card(
    parent: tk.Widget,
    *,
    on_export_x,
    on_export_youtube,
) -> dict[str, tk.Button]:
    """Build the export action area."""
    button_frame = tk.Frame(parent)
    button_frame.pack()

    x_button = tk.Button(
        button_frame,
        text="Export for X (512 MB)",
        width=34,
        command=on_export_x,
    )
    x_button.pack(pady=(0, 8))

    youtube_button = tk.Button(
        button_frame,
        text="Export for YouTube (High Quality)",
        width=34,
        command=on_export_youtube,
    )
    youtube_button.pack()

    return {
        "x_button": x_button,
        "youtube_button": youtube_button,
    }
