"""Recent exports UI component for Exile Creator Kit."""

import tkinter as tk

from gui.components.theme import (
    BACKGROUND,
    BORDER,
    CARD_BACKGROUND,
    FONT_HEADING,
    FONT_SMALL,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


def build_recent_exports_card(
    parent: tk.Widget,
    *,
    recent_exports_text: tk.StringVar,
) -> tk.Frame:
    """Build the recent exports area."""
    outer_frame = tk.Frame(parent, bg=BACKGROUND)
    outer_frame.pack(fill=tk.X, padx=14, pady=8)

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

    recent_exports_heading = tk.Label(
        frame,
        text="Recent Exports",
        bg=CARD_BACKGROUND,
        fg=TEXT_PRIMARY,
        font=FONT_HEADING,
    )
    recent_exports_heading.pack(anchor=tk.W, padx=24, pady=(22, 8))

    recent_exports_label = tk.Label(
        frame,
        textvariable=recent_exports_text,
        justify=tk.LEFT,
        bg=CARD_BACKGROUND,
        fg=TEXT_SECONDARY,
        font=FONT_SMALL,
    )
    recent_exports_label.pack(anchor=tk.W, padx=24, pady=(0, 22))

    return outer_frame
