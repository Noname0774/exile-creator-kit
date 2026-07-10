"""Export status UI component for Exile Creator Kit."""

import tkinter as tk
from tkinter import ttk


def build_status_card(
    parent: tk.Widget,
    *,
    export_status: tk.StringVar,
    export_message: tk.StringVar,
    on_open_output_folder,
    on_open_log_folder,
) -> dict[str, tk.Widget]:
    """Build the export status area."""
    status_heading = tk.Label(parent, text="Status", font=("Segoe UI", 11, "bold"))
    status_heading.pack(anchor=tk.W, padx=40)

    status_label = tk.Label(parent, textvariable=export_status)
    status_label.pack(pady=(8, 6))

    progress_bar = ttk.Progressbar(parent, mode="indeterminate", length=280)
    progress_bar.pack()

    message_label = tk.Label(parent, textvariable=export_message)
    message_label.pack(pady=(8, 0))

    open_output_button = tk.Button(
        parent,
        text="Open Output Folder",
        width=22,
        state=tk.DISABLED,
        command=on_open_output_folder,
    )
    open_output_button.pack(pady=(8, 0))

    open_log_button = tk.Button(
        parent,
        text="Open Log Folder",
        width=22,
        state=tk.DISABLED,
        command=on_open_log_folder,
    )
    open_log_button.pack(pady=(8, 0))

    return {
        "progress_bar": progress_bar,
        "open_output_button": open_output_button,
        "open_log_button": open_log_button,
    }
