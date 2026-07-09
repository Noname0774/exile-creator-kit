"""About dialog for Exile Creator Kit."""

from pathlib import Path
import sys
import tkinter as tk


def get_version() -> str:
    """Return the canonical application version."""
    candidates = [
        Path(getattr(sys, "_MEIPASS", "")) / "VERSION",
        Path(sys.executable).resolve().parent / "VERSION",
        Path(__file__).resolve().parents[1] / "VERSION",
    ]

    for version_file in candidates:
        try:
            version = version_file.read_text(encoding="utf-8").strip()
        except OSError:
            continue

        if version:
            return version

    return "unknown"


def create_about_window() -> tk.Toplevel:
    """Create the About dialog."""
    window = tk.Toplevel()
    window.title("About")
    window.geometry("360x260")
    window.resizable(False, False)

    title = tk.Label(window, text="About", font=("Segoe UI", 16, "bold"))
    title.pack(pady=(20, 14))

    content = tk.Label(
        window,
        text=(
            "Application name:\n"
            "Exile Creator Kit\n\n"
            "Version:\n"
            f"{get_version()}\n\n"
            "Description:\n"
            "Create upload-ready videos for X and YouTube.\n\n"
            "Author:\n"
            "Open Source"
        ),
        justify=tk.LEFT,
    )
    content.pack(anchor=tk.W, padx=36)

    return window
