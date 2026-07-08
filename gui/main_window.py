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
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.media.inspector import MediaInspector  # noqa: E402

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
    window.geometry("460x560")
    selected_file_name = tk.StringVar(value="Drop video here")
    selected_file_path = tk.StringVar(value="")
    media_info_text = tk.StringVar(value="")
    export_status = tk.StringVar(value="Idle")
    export_message = tk.StringVar(value="")

    def get_output_filename(file_path: str, script_name: str) -> str:
        path = Path(file_path)
        suffix = "_youtube" if script_name == "export_to_youtube.py" else "_x"
        return f"{path.stem}{suffix}.mp4"

    def set_export_buttons_enabled(is_enabled: bool) -> None:
        state = tk.NORMAL if is_enabled else tk.DISABLED
        x_button.config(state=state)
        youtube_button.config(state=state)

    def format_file_size(file_size_mb: float) -> str:
        if file_size_mb >= 1024:
            return f"{file_size_mb / 1024:.2f} GB"

        return f"{file_size_mb:.2f} MB"

    def set_media_info(file_path: str) -> None:
        try:
            media_info = MediaInspector().analyze(file_path)
        except RuntimeError:
            media_info_text.set("Media information unavailable.")
            return

        path = Path(file_path)
        media_info_text.set(
            f"File: {path.name}\n"
            f"Location: {path.parent}\n"
            f"Duration: {media_info.duration_text}\n"
            f"Resolution: {media_info.width} × {media_info.height}\n"
            f"File size: {format_file_size(media_info.file_size_mb)}"
        )

    def set_selected_file(file_path: str) -> None:
        path = Path(file_path)
        if path.suffix.lower() not in SUPPORTED_VIDEO_EXTENSIONS:
            messagebox.showinfo("Exile Creator Kit", "Please choose a video file.")
            return

        selected_file_path.set(str(path))
        selected_file_name.set(path.name)
        set_media_info(str(path))

    def export_selected(script_name: str) -> None:
        file_path = selected_file_path.get()
        if not file_path:
            export_status.set("Failed")
            export_message.set("No video selected.")
            messagebox.showinfo("Exile Creator Kit", "Please choose a video first.")
            return

        if shutil.which("ffmpeg") is None:
            export_status.set("Failed")
            export_message.set(
                "FFmpeg was not found.\n"
                "Please install FFmpeg and restart Exile Creator Kit."
            )
            return

        export_status.set("Preparing...")
        export_message.set("")
        set_export_buttons_enabled(False)
        progress_bar.start(10)

        try:
            process = launch_export_workflow(script_name, file_path)
        except OSError:
            progress_bar.stop()
            set_export_buttons_enabled(True)
            export_status.set("Failed")
            export_message.set("Unknown error.")
            return

        window.after(500, lambda: export_status.set("Encoding..."))
        output_filename = get_output_filename(file_path, script_name)
        window.after(1000, lambda: watch_export(process, output_filename))

    def watch_export(process: subprocess.Popen, output_filename: str) -> None:
        if process.poll() is None:
            window.after(1000, lambda: watch_export(process, output_filename))
            return

        progress_bar.stop()
        set_export_buttons_enabled(True)
        if process.returncode == 0:
            export_status.set("Completed")
            export_message.set(f"Saved as:\n{output_filename}")
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

    def register_drop_target(widget: tk.Widget) -> None:
        if TkinterDnD:
            widget.drop_target_register(DND_FILES)
            widget.dnd_bind("<<Drop>>", handle_drop)

    def add_separator() -> None:
        separator = ttk.Separator(window, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, padx=28, pady=14)

    register_drop_target(window)

    title = tk.Label(window, text="Exile Creator Kit", font=("Segoe UI", 18, "bold"))
    title.pack(pady=(24, 6))

    description = tk.Label(window, text="Create upload-ready videos for X and YouTube")
    description.pack()

    add_separator()

    selected_video_heading = tk.Label(
        window,
        text="Selected Video",
        font=("Segoe UI", 11, "bold"),
    )
    selected_video_heading.pack(anchor=tk.W, padx=40, pady=(0, 8))

    drop_area = tk.Label(
        window,
        textvariable=selected_file_name,
        relief="groove",
        width=42,
        height=3,
    )
    drop_area.pack(pady=(0, 10))
    register_drop_target(drop_area)

    media_info_label = tk.Label(window, textvariable=media_info_text, justify=tk.LEFT)
    media_info_label.pack(anchor=tk.W, padx=54, pady=(0, 4))

    add_separator()

    choose_button = tk.Button(window, text="Choose Video", width=22, command=choose_video)
    choose_button.pack(pady=(0, 2))

    add_separator()

    button_frame = tk.Frame(window)
    button_frame.pack()

    x_button = tk.Button(
        button_frame,
        text="Export for X (512 MB)",
        width=34,
        command=lambda: export_selected("export_to_x.py"),
    )
    x_button.pack(pady=(0, 8))

    youtube_button = tk.Button(
        button_frame,
        text="Export for YouTube (High Quality)",
        width=34,
        command=lambda: export_selected("export_to_youtube.py"),
    )
    youtube_button.pack()

    add_separator()

    status_heading = tk.Label(window, text="Status", font=("Segoe UI", 11, "bold"))
    status_heading.pack(anchor=tk.W, padx=40)

    status_label = tk.Label(window, textvariable=export_status)
    status_label.pack(pady=(8, 6))

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
