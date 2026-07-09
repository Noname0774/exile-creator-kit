"""Settings window prototype."""

import tkinter as tk
from tkinter import ttk


SETTINGS_SECTIONS = ("General", "X Export", "YouTube Export", "FFmpeg", "GUI")


def create_settings_window() -> tk.Toplevel:
    """Create the settings prototype window."""
    window = tk.Toplevel()
    window.title("Settings")
    window.geometry("360x320")

    title = tk.Label(window, text="Settings", font=("Segoe UI", 16, "bold"))
    title.pack(pady=(20, 12))

    for section_name in SETTINGS_SECTIONS:
        section_label = tk.Label(window, text=section_name, font=("Segoe UI", 11, "bold"))
        section_label.pack(anchor=tk.W, padx=36, pady=(8, 4))

        separator = ttk.Separator(window, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, padx=36)

    return window


def main() -> None:
    root = tk.Tk()
    root.withdraw()
    create_settings_window()
    root.mainloop()


if __name__ == "__main__":
    main()
