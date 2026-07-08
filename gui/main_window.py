"""Prototype GUI window for Exile Creator Kit."""

import shutil
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    DND_FILES = ""
    TkinterDnD = None


ROOT_DIR = Path(__file__).resolve().parents[1]
SUPPORTED_VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov", ".avi"}


def launch_export_workflow(script_name: str, file_path: str) -> subprocess.Popen:
    """Launch the existing export entry workflow."""
    script_path = ROOT_DIR / "tools" / script_name
    return subprocess.Popen(
        [sys.executable, str(script_path), file_path],
        cwd=ROOT_DIR,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )


def create_window() -> tk.Tk:
    """Create the prototype main window."""
    window = TkinterDnD.Tk() if TkinterDnD else tk.Tk()
    window.title("Exile Creator Kit")
    window.geometry("420x320")
    selected_file_name = tk.StringVar(value="Drop video here")
    selected_file_path = tk.StringVar(value="")
    export_status = tk.StringVar(value="Idle")
    export_message = tk.StringVar(value="")

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
            export_status.set("Failed")
            export_message.set("No video selected.")
            messagebox.showinfo("Exile Creator Kit", "Please choose a video first.")
            return

        if shutil.which("ffmpeg") is None:
            export_status.set("Failed")
            export_message.set("FFmpeg not found.")
            return

        export_status.set("Preparing...")
        export_message.set("")
        progress_bar.start(10)

        try:
            process = launch_export_workflow(script_name, file_path)
        except OSError:
            progress_bar.stop()
            export_status.set("Failed")
            export_message.set("Unknown error.")
            return

        window.after(500, lambda: export_status.set("Encoding..."))
        window.after(1000, lambda: watch_export(process))

    def watch_export(process: subprocess.Popen) -> None:
        if process.poll() is None:
            window.after(1000, lambda: watch_export(process))
            return

        progress_bar.stop()
        if process.returncode == 0:
            export_status.set("Completed")
            export_message.set("")
        else:
            export_status.set("Failed")
            export_message.set("Export failed.")

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

    status_label = tk.Label(window, textvariable=export_status)
    status_label.pack(pady=(18, 6))

    progress_bar = ttk.Progressbar(window, mode="indeterminate", length=280)
    progress_bar.pack()

    message_label = tk.Label(window, textvariable=export_message)
    message_label.pack(pady=(8, 0))

    return window


def main() -> None:
    """Run the prototype window."""
    create_window().mainloop()


if __name__ == "__main__":
    main()
