"""Recent exports UI component for Exile Creator Kit."""

import tkinter as tk


def build_recent_exports_card(
    parent: tk.Widget,
    *,
    recent_exports_text: tk.StringVar,
) -> tk.Frame:
    """Build the recent exports area."""
    frame = tk.Frame(parent)
    frame.pack(fill=tk.X)

    recent_exports_heading = tk.Label(
        frame,
        text="Recent Exports",
        font=("Segoe UI", 11, "bold"),
    )
    recent_exports_heading.pack(anchor=tk.W, padx=40)

    recent_exports_label = tk.Label(
        frame,
        textvariable=recent_exports_text,
        justify=tk.LEFT,
    )
    recent_exports_label.pack(anchor=tk.W, padx=54, pady=(8, 0))

    return frame
