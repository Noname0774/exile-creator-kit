"""Selected media UI component for Exile Creator Kit."""

import tkinter as tk


def build_media_card(
    parent: tk.Widget,
    *,
    selected_file_name: tk.StringVar,
    media_info_text: tk.StringVar,
    on_choose_video,
    register_drop_target,
) -> tk.Frame:
    """Build the selected video area."""
    frame = tk.Frame(parent)
    frame.pack()

    selected_video_heading = tk.Label(
        frame,
        text="Selected Video",
        font=("Segoe UI", 11, "bold"),
    )
    selected_video_heading.pack(anchor=tk.W, padx=40, pady=(0, 8))

    drop_area = tk.Label(
        frame,
        textvariable=selected_file_name,
        relief="groove",
        width=42,
        height=3,
    )
    drop_area.pack(pady=(0, 10))
    register_drop_target(drop_area)

    media_info_label = tk.Label(frame, textvariable=media_info_text, justify=tk.LEFT)
    media_info_label.pack(anchor=tk.W, padx=54, pady=(0, 4))

    choose_button = tk.Button(
        frame,
        text="Choose Video",
        width=22,
        command=on_choose_video,
    )
    choose_button.pack(pady=(0, 2))

    return frame
