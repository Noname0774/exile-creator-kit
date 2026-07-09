"""Prototype GUI window for Exile Creator Kit."""

from datetime import datetime
import os
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

from core.export import ExportHistory, ExportJob, ExportQueue, HistoryEntry  # noqa: E402
from core.media.inspector import MediaInspector  # noqa: E402
from core.settings import SettingsService  # noqa: E402
from gui.about_window import create_about_window  # noqa: E402
from gui.settings_window import create_settings_window  # noqa: E402
from tools.export_to_x import x_output_path  # noqa: E402
from tools.export_to_youtube import youtube_output_path  # noqa: E402

SUPPORTED_VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov", ".avi"}


def launch_export_workflow(
    script_name: str,
    file_path: str,
    output_path: str,
) -> subprocess.Popen:
    """Launch the existing export entry workflow."""
    script_path = ROOT_DIR / "tools" / script_name
    return subprocess.Popen(
        [sys.executable, str(script_path), file_path, output_path],
        cwd=ROOT_DIR,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )


def create_window() -> tk.Tk:
    """Create the prototype main window."""
    window = TkinterDnD.Tk() if TkinterDnD else tk.Tk()
    window.title("Exile Creator Kit")
    window.geometry("460x680")
    selected_file_name = tk.StringVar(value="Drop video here")
    selected_file_path = tk.StringVar(value="")
    media_info_text = tk.StringVar(value="")
    export_status = tk.StringVar(value="Idle")
    export_message = tk.StringVar(value="")
    recent_exports_text = tk.StringVar(value="No exports yet.")

    export_history = ExportHistory()
    export_queue = ExportQueue()
    settings_service = SettingsService()
    app_settings = settings_service.get_settings()
    output_folder_path = tk.StringVar(value="")

    def reload_settings() -> None:
        nonlocal app_settings
        app_settings = settings_service.get_settings()

    def get_last_selected_folder() -> str:
        if app_settings.remember_last_selected_folder:
            folder_path = app_settings.last_selected_folder
            if folder_path and Path(folder_path).exists():
                return folder_path

        output_folder = app_settings.default_output_folder
        if output_folder and Path(output_folder).exists():
            return output_folder

        return ""

    def save_last_selected_folder(file_path: str) -> None:
        nonlocal app_settings
        if not app_settings.remember_last_selected_folder:
            return

        app_settings = settings_service.update_settings(
            last_selected_folder=str(Path(file_path).parent)
        )

    def get_export_target(script_name: str) -> str:
        if script_name == "export_to_youtube.py":
            return "YouTube"

        return "X"

    def get_export_script(target: str) -> str:
        if target == "YouTube":
            return "export_to_youtube.py"

        return "export_to_x.py"

    def get_output_path(file_path: str, target: str) -> Path:
        if target == "YouTube":
            return youtube_output_path(file_path)

        return x_output_path(file_path)

    def refresh_recent_exports() -> None:
        entries = export_history.entries()
        if not entries:
            recent_exports_text.set("No exports yet.")
            return

        recent_exports_text.set(
            "\n".join(
                f"{Path(entry.output_path).name} | "
                f"{entry.target} | "
                f"{entry.status} | "
                f"{entry.timestamp}"
                for entry in reversed(entries[-5:])
            )
        )

    def add_recent_export(job: ExportJob) -> None:
        export_history.add(
            HistoryEntry(
                input_path=job.input_path,
                output_path=job.output_path,
                target=job.target,
                status=job.status,
                timestamp=datetime.now().strftime("%H:%M"),
            )
        )
        refresh_recent_exports()

    def set_export_buttons_enabled(is_enabled: bool) -> None:
        state = tk.NORMAL if is_enabled else tk.DISABLED
        x_button.config(state=state)
        youtube_button.config(state=state)

    def set_open_output_button_enabled(is_enabled: bool) -> None:
        state = tk.NORMAL if is_enabled else tk.DISABLED
        open_output_button.config(state=state)

    def open_folder(folder_path: str) -> None:
        if not folder_path:
            return

        try:
            os.startfile(folder_path)
        except OSError:
            messagebox.showinfo("Exile Creator Kit", "Output folder could not be opened.")

    def open_output_folder() -> None:
        open_folder(output_folder_path.get())

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
        save_last_selected_folder(str(path))

    def is_ffmpeg_available() -> bool:
        availability_check = getattr(settings_service, "is_ffmpeg_available", None)
        if callable(availability_check):
            return bool(availability_check())

        return bool(settings_service.get_ffmpeg_path())

    def export_selected(script_name: str) -> None:
        file_path = selected_file_path.get()
        if not file_path:
            export_status.set("Failed")
            export_message.set("No video selected.")
            messagebox.showinfo("Exile Creator Kit", "Please choose a video first.")
            return

        if not is_ffmpeg_available():
            export_status.set("Failed")
            export_message.set(
                "FFmpeg was not found.\n"
                "Please install FFmpeg and restart Exile Creator Kit."
            )
            return

        export_status.set("Preparing...")
        export_message.set("")
        output_folder_path.set("")
        set_export_buttons_enabled(False)
        set_open_output_button_enabled(False)
        progress_bar.start(10)

        target = get_export_target(script_name)
        output_path = get_output_path(file_path, target)
        export_queue.add(
            ExportJob(
                input_path=file_path,
                output_path=str(output_path),
                target=target,
                status="Queued",
            )
        )
        queued_job = export_queue.pop()
        if queued_job is None:
            progress_bar.stop()
            set_export_buttons_enabled(True)
            export_status.set("Failed")
            export_message.set("Unknown error.")
            return

        script_name = get_export_script(queued_job.target)
        try:
            process = launch_export_workflow(
                script_name,
                queued_job.input_path,
                queued_job.output_path,
            )
        except OSError:
            progress_bar.stop()
            set_export_buttons_enabled(True)
            export_status.set("Failed")
            export_message.set("Unknown error.")
            return

        window.after(500, lambda: export_status.set("Encoding..."))
        window.after(1000, lambda: watch_export(process, queued_job))

    def watch_export(process: subprocess.Popen, job: ExportJob) -> None:
        if process.poll() is None:
            window.after(1000, lambda: watch_export(process, job))
            return

        progress_bar.stop()
        set_export_buttons_enabled(True)
        if process.returncode == 0:
            export_status.set("Completed")
            output_path = Path(job.output_path)
            completed_job = ExportJob(
                input_path=job.input_path,
                output_path=job.output_path,
                target=job.target,
                status="Completed",
            )
            output_folder_path.set(str(output_path.parent))
            set_open_output_button_enabled(True)
            export_message.set(f"Saved to:\n{output_path}")
            add_recent_export(completed_job)
            if app_settings.open_output_folder_after_export:
                open_folder(str(output_path.parent))
        else:
            export_status.set("Failed")
            set_open_output_button_enabled(False)
            export_message.set("Export failed.")
            failed_job = ExportJob(
                input_path=job.input_path,
                output_path=job.output_path,
                target=job.target,
                status="Failed",
            )
            add_recent_export(failed_job)

    def choose_video() -> None:
        file_path = filedialog.askopenfilename(
            title="Choose a video file",
            initialdir=get_last_selected_folder(),
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

    def open_settings_window() -> None:
        create_settings_window(on_saved=reload_settings)

    def open_about_window() -> None:
        create_about_window()

    register_drop_target(window)

    title = tk.Label(window, text="Exile Creator Kit", font=("Segoe UI", 18, "bold"))
    title.pack(pady=(24, 6))

    description = tk.Label(window, text="Create upload-ready videos for X and YouTube")
    description.pack()

    app_button_frame = tk.Frame(window)
    app_button_frame.pack(pady=(10, 0))

    settings_button = tk.Button(
        app_button_frame,
        text="Settings",
        width=16,
        command=open_settings_window,
    )
    settings_button.pack(side=tk.LEFT, padx=4)

    about_button = tk.Button(
        app_button_frame,
        text="About",
        width=16,
        command=open_about_window,
    )
    about_button.pack(side=tk.LEFT, padx=4)

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

    open_output_button = tk.Button(
        window,
        text="Open Output Folder",
        width=22,
        state=tk.DISABLED,
        command=open_output_folder,
    )
    open_output_button.pack(pady=(8, 0))

    add_separator()

    recent_exports_heading = tk.Label(
        window,
        text="Recent Exports",
        font=("Segoe UI", 11, "bold"),
    )
    recent_exports_heading.pack(anchor=tk.W, padx=40)

    recent_exports_label = tk.Label(
        window,
        textvariable=recent_exports_text,
        justify=tk.LEFT,
    )
    recent_exports_label.pack(anchor=tk.W, padx=54, pady=(8, 0))

    return window


def main() -> None:
    """Run the prototype window."""
    create_window().mainloop()


if __name__ == "__main__":
    main()
