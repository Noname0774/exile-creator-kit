"""Prototype GUI window for Exile Creator Kit."""

import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    DND_FILES = ""
    TkinterDnD = None


ROOT_DIR = Path(__file__).resolve().parents[1]
SUPPORTED_VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov", ".avi"}


def launch_export_workflow(script_name: str, file_path: str) -> None:
    """Launch the existing export entry workflow."""
    script_path = ROOT_DIR / "tools" / script_name
    subprocess.Popen(
        ["cmd", "/c", "start", "", sys.executable, str(script_path), file_path],
        cwd=ROOT_DIR,
    )


def create_window() -> tk.Tk:
    """Create the prototype main window."""
    window = TkinterDnD.Tk() if TkinterDnD else tk.Tk()
    window.title("Exile Creator Kit")
    window.geometry("420x260")
    selected_file_name = tk.StringVar(value="Drop video here")
    selected_file_path = tk.StringVar(value="")

    def set_selected_file(file_path: str) -> None:
        path = Path(file_path)
        if path.suffix.lower() not in SUPPORTED_VIDEO_EXTENSIONS:
            messagebox.showinfo("Exile Creator Kit", "Please choose a video file.")
            return

        selected_file_path.set(str(path))
        selected_file_name.set(path.name)

    def export_selected(script_name: str) -> None:
        file_path = selected_file_path.get()
        if not file_path:
            messagebox.showinfo("Exile Creator Kit", "Please choose a video first.")
            return

        launch_export_workflow(script_name, file_path)

    def choose_video() -> None:
        file_path = filedialog.askopenfilename(
            title="Choose a video file",
            filetypes=[
                ("Video files", "*.mp4 *.mkv *.mov *.avi"),
                ("MP4 files", "*.mp4"),
                ("MKV files", "*.mkv"),
                ("MOV files", "*.mov"),
                ("AVI files", "*.avi"),
            ],
        )
        if file_path:
            set_selected_file(file_path)

    def handle_drop(event) -> None:
        dropped_paths = window.tk.splitlist(event.data)
        if dropped_paths:
            set_selected_file(dropped_paths[0])

    title = tk.Label(window, text="Exile Creator Kit", font=("Segoe UI", 18, "bold"))
    title.pack(pady=(28, 20))

    drop_area = tk.Label(
        window,
        textvariable=selected_file_name,
        relief="groove",
        width=34,
        height=3,
    )
    drop_area.pack(pady=(0, 10))
    if TkinterDnD:
        drop_area.drop_target_register(DND_FILES)
        drop_area.dnd_bind("<<Drop>>", handle_drop)

    choose_button = tk.Button(window, text="Choose Video", width=18, command=choose_video)
    choose_button.pack(pady=(0, 18))

    button_frame = tk.Frame(window)
    button_frame.pack()

    x_button = tk.Button(
        button_frame,
        text="X Export",
        width=16,
        command=lambda: export_selected("export_to_x.py"),
    )
    x_button.pack(side=tk.LEFT, padx=8)

    youtube_button = tk.Button(
        button_frame,
        text="YouTube Export",
        width=16,
        command=lambda: export_selected("export_to_youtube.py"),
    )
    youtube_button.pack(side=tk.LEFT, padx=8)

    return window


def main() -> None:
    """Run the prototype window."""
    create_window().mainloop()


if __name__ == "__main__":
    main()
