"""Prototype GUI window for Exile Creator Kit."""

from datetime import datetime
import os
import re
import subprocess
import sys
import threading
import tkinter as tk
import traceback
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
from core.export import XExporter, YouTubeExporter  # noqa: E402
from core.media.inspector import MediaInspector  # noqa: E402
from core.media.smart_bitrate import SmartBitrate  # noqa: E402
from core.settings import SettingsService  # noqa: E402
from gui.about_window import create_about_window  # noqa: E402
from gui.components.export_card import build_export_card  # noqa: E402
from gui.components.header import build_header  # noqa: E402
from gui.components.media_card import build_media_card  # noqa: E402
from gui.components.recent_exports_card import build_recent_exports_card  # noqa: E402
from gui.components.status_card import build_status_card  # noqa: E402
from gui.components.theme import BACKGROUND  # noqa: E402
from gui.settings_window import create_settings_window  # noqa: E402
from tools.export_to_x import x_output_path  # noqa: E402
from tools.export_to_youtube import youtube_output_path  # noqa: E402

SUPPORTED_VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov", ".avi"}
ENCODER_AUTO = "Auto (Recommended)"
ENCODER_NVENC = "NVIDIA NVENC"
ENCODER_SOFTWARE = "Software (libx264)"
SOFTWARE_ENCODER_PREFERRED = False


class ExportWorker:
    """Run an export in the background without assuming a source checkout."""

    def __init__(
        self,
        target: str,
        input_path: str,
        output_path: str,
        encoder_setting: str,
    ) -> None:
        self.target = target
        self.input_path = input_path
        self.output_path = output_path
        self.encoder_setting = encoder_setting
        self.returncode: int | None = None
        self.command = ""
        self.stdout = ""
        self.stderr = ""
        self.traceback_text = ""
        self.first_command = ""
        self.first_returncode: int | None = None
        self.first_stdout = ""
        self.first_stderr = ""
        self.fallback_command = ""
        self.fallback_returncode: int | None = None
        self.fallback_stdout = ""
        self.fallback_stderr = ""
        self.fallback_started = False
        self.fallback_used = False
        self.software_encoder_preferred = False
        self.actual_encoder_used = ""
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self) -> None:
        self._thread.start()

    def poll(self) -> int | None:
        if self._thread.is_alive():
            return None

        return self.returncode

    def communicate(self) -> tuple[str, str]:
        return self.stdout, self.stderr

    def _run_command(self, command: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            command,
            capture_output=True,
            shell=True,
            text=True,
        )

    def _software_fallback_command(self, command: str) -> str:
        fallback_command = re.sub(
            r'(-c:v\s+)(?:"[^"]+"|\S+)',
            r"\1libx264",
            command,
            count=1,
        )
        fallback_command = re.sub(
            r'(-preset\s+)(?:"[^"]+"|\S+)',
            r"\1medium",
            fallback_command,
            count=1,
        )
        return re.sub(
            r'\s-cq\s+(?:"[^"]+"|\S+)',
            "",
            fallback_command,
            count=1,
        )

    def _video_encoder_from_command(self, command: str) -> str:
        match = re.search(r'-c:v\s+(?:"([^"]+)"|(\S+))', command)
        if not match:
            return "unknown"

        return match.group(1) or match.group(2) or "unknown"

    def _run(self) -> None:
        global SOFTWARE_ENCODER_PREFERRED

        try:
            media_info = MediaInspector().analyze(self.input_path)
            if self.target == "YouTube":
                self.command = YouTubeExporter().export(
                    self.input_path,
                    self.output_path,
                )
            else:
                bitrate = SmartBitrate().calculate(media_info.duration_seconds)
                self.command = XExporter().export(
                    self.input_path,
                    self.output_path,
                    bitrate,
                )

            if self.encoder_setting == ENCODER_SOFTWARE:
                self.command = self._software_fallback_command(self.command)
            elif self.encoder_setting == ENCODER_AUTO and SOFTWARE_ENCODER_PREFERRED:
                self.command = self._software_fallback_command(self.command)
                self.software_encoder_preferred = True

            self.first_command = self.command
            first_result = self._run_command(self.first_command)
            self.first_returncode = first_result.returncode
            self.first_stdout = first_result.stdout
            self.first_stderr = first_result.stderr
            self.actual_encoder_used = self._video_encoder_from_command(self.first_command)

            if first_result.returncode == 0:
                self.stdout = first_result.stdout
                self.stderr = first_result.stderr
                self.returncode = 0
                return

            if self.encoder_setting != ENCODER_AUTO or self.software_encoder_preferred:
                self.stdout = first_result.stdout
                self.stderr = first_result.stderr
                self.returncode = first_result.returncode
                return

            self.fallback_started = True
            self.fallback_command = self._software_fallback_command(self.first_command)
            self.command = self.fallback_command
            self.actual_encoder_used = self._video_encoder_from_command(
                self.fallback_command
            )
            fallback_result = self._run_command(self.fallback_command)
            self.fallback_returncode = fallback_result.returncode
            self.fallback_stdout = fallback_result.stdout
            self.fallback_stderr = fallback_result.stderr
            self.stdout = fallback_result.stdout
            self.stderr = fallback_result.stderr
            self.returncode = fallback_result.returncode
            self.fallback_used = fallback_result.returncode == 0
            if self.fallback_used:
                SOFTWARE_ENCODER_PREFERRED = True
        except Exception as exc:
            self.stderr = str(exc)
            self.traceback_text = traceback.format_exc()
            self.returncode = 1


def launch_export_workflow(
    script_name: str,
    file_path: str,
    output_path: str,
    encoder_setting: str,
) -> ExportWorker:
    """Launch the existing export workflow."""
    target = "YouTube" if script_name == "export_to_youtube.py" else "X"
    worker = ExportWorker(target, file_path, output_path, encoder_setting)
    worker.start()
    return worker


def create_window() -> tk.Tk:
    """Create the prototype main window."""
    window = TkinterDnD.Tk() if TkinterDnD else tk.Tk()
    window.title("Exile Creator Kit")
    window.geometry("900x780")
    window.minsize(760, 620)
    window.configure(bg=BACKGROUND)

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
    log_folder_path = tk.StringVar(value="")

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

    def set_open_log_button_enabled(is_enabled: bool) -> None:
        state = tk.NORMAL if is_enabled else tk.DISABLED
        open_log_button.config(state=state)

    def get_log_folder() -> Path:
        app_data = os.environ.get("APPDATA")
        if app_data:
            return Path(app_data) / "ExileCreatorKit" / "logs"

        return Path.home() / ".exile-creator-kit" / "logs"

    def next_export_log_path(log_folder: Path) -> Path:
        date_text = datetime.now().strftime("%Y-%m-%d")
        for index in range(1, 1000):
            candidate = log_folder / f"export-{date_text}-{index:03d}.log"
            if not candidate.exists():
                return candidate

        time_text = datetime.now().strftime("%H%M%S")
        return log_folder / f"export-{date_text}-{time_text}.log"

    def get_application_version() -> str:
        version_path = ROOT_DIR / "VERSION"
        try:
            return version_path.read_text(encoding="utf-8").strip() or "unknown"
        except OSError:
            return "unknown"

    def write_export_failure_log(
        process: ExportWorker,
        job: ExportJob,
        stdout: str,
        stderr: str,
    ) -> Path | None:
        try:
            log_folder = get_log_folder()
            log_folder.mkdir(parents=True, exist_ok=True)
            log_path = next_export_log_path(log_folder)
            log_path.write_text(
                "\n".join(
                    [
                        "Exile Creator Kit Export Failure",
                        f"Version: {get_application_version()}",
                        f"Timestamp: {datetime.now().isoformat(timespec='seconds')}",
                        "",
                        "Python traceback:",
                        process.traceback_text.strip() or "(not available)",
                        "",
                        f"Selected preset: {job.target}",
                        f"Selected encoder setting: {process.encoder_setting}",
                        f"Actual encoder used: {process.actual_encoder_used or 'unknown'}",
                        f"Fallback used: {process.fallback_used}",
                        f"Input file: {job.input_path}",
                        f"Output file: {job.output_path}",
                        "",
                        "First command:",
                        process.first_command or process.command or "(command was not generated)",
                        f"First exit code: {process.first_returncode}",
                        "",
                        "First stdout:",
                        process.first_stdout or stdout or "(empty)",
                        "",
                        "First stderr:",
                        process.first_stderr or stderr or "(empty)",
                        "",
                        "Fallback command:",
                        process.fallback_command or "(fallback was not generated)",
                        f"Fallback exit code: {process.fallback_returncode}",
                        "",
                        "Fallback stdout:",
                        process.fallback_stdout or "(empty)",
                        "",
                        "Fallback stderr:",
                        process.fallback_stderr or "(empty)",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            return log_path
        except OSError:
            return None

    def write_export_success_log(process: ExportWorker, job: ExportJob) -> Path | None:
        try:
            log_folder = get_log_folder()
            log_folder.mkdir(parents=True, exist_ok=True)
            log_path = next_export_log_path(log_folder)
            log_path.write_text(
                "\n".join(
                    [
                        "Exile Creator Kit Export Success",
                        f"Version: {get_application_version()}",
                        f"Timestamp: {datetime.now().isoformat(timespec='seconds')}",
                        f"Export target: {job.target}",
                        f"Selected encoder setting: {process.encoder_setting}",
                        f"Actual video codec used: {process.actual_encoder_used or 'unknown'}",
                        f"Output file: {job.output_path}",
                        "",
                        "FFmpeg command:",
                        process.command or "(command was not generated)",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            return log_path
        except OSError:
            return None

    def user_friendly_error(error: object) -> str:
        raw_message = str(error).strip()
        message = raw_message.lower()

        if "ffmpeg" in message and ("not found" in message or "is not recognized" in message):
            return (
                "FFmpeg was not found.\n"
                "Please install FFmpeg or update the FFmpeg path in Settings."
            )

        if "ffprobe" in message and ("not found" in message or "is not recognized" in message):
            return (
                "FFprobe was not found.\n"
                "Please install FFmpeg or update the FFprobe path in Settings."
            )

        if "permission denied" in message or "access is denied" in message:
            return (
                "Permission denied.\n"
                "Please choose a different output folder or check folder permissions."
            )

        if (
            "output folder unavailable" in message
            or "no such file" in message
            or "cannot find the path" in message
        ):
            return (
                "Output folder unavailable.\n"
                "Please choose an existing output folder in Settings."
            )

        if (
            "invalid data" in message
            or "moov atom not found" in message
            or "could not find codec parameters" in message
        ):
            return (
                "Invalid video file.\n"
                "Please choose a playable video file and try again."
            )

        if raw_message:
            return (
                "Export failed.\n"
                "Please check the selected video and export settings, then try again."
            )

        return (
            "Export failed for an unknown reason.\n"
            "Please try another video or check your export settings."
        )

    def set_failed_status(error: object) -> None:
        export_status.set("Failed")
        export_message.set(user_friendly_error(error))

    def open_folder(folder_path: str) -> None:
        if not folder_path:
            return

        try:
            os.startfile(folder_path)
        except OSError:
            messagebox.showinfo(
                "Exile Creator Kit",
                "Output folder unavailable.\n"
                "Please check that the folder exists and try again.",
            )

    def open_output_folder() -> None:
        open_folder(output_folder_path.get())

    def open_log_folder() -> None:
        open_folder(log_folder_path.get())

    def format_file_size(file_size_mb: float) -> str:
        if file_size_mb >= 1024:
            return f"{file_size_mb / 1024:.2f} GB"

        return f"{file_size_mb:.2f} MB"

    def set_media_info(file_path: str) -> None:
        try:
            media_info = MediaInspector().analyze(file_path)
        except RuntimeError as exc:
            media_info_text.set(user_friendly_error(exc))
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
            set_failed_status("FFmpeg was not found.")
            return

        export_status.set("Preparing...")
        export_message.set("")
        output_folder_path.set("")
        log_folder_path.set("")
        set_export_buttons_enabled(False)
        set_open_output_button_enabled(False)
        set_open_log_button_enabled(False)
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
            set_failed_status("")
            return

        script_name = get_export_script(queued_job.target)
        output_parent = Path(queued_job.output_path).parent
        if not output_parent.exists():
            progress_bar.stop()
            set_export_buttons_enabled(True)
            set_failed_status("Output folder unavailable.")
            return

        if not os.access(output_parent, os.W_OK):
            progress_bar.stop()
            set_export_buttons_enabled(True)
            set_failed_status("Permission denied.")
            return

        try:
            process = launch_export_workflow(
                script_name,
                queued_job.input_path,
                queued_job.output_path,
                app_settings.encoder,
            )
        except OSError as exc:
            progress_bar.stop()
            set_export_buttons_enabled(True)
            set_failed_status(exc)
            return

        window.after(500, lambda: export_status.set("Encoding..."))
        window.after(1000, lambda: watch_export(process, queued_job))

    def watch_export(process: ExportWorker, job: ExportJob) -> None:
        if process.poll() is None:
            if process.fallback_started:
                export_message.set(
                    "Hardware encoder failed. Retrying with software encoder..."
                )
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
                status="Completed (software fallback)"
                if process.fallback_used
                else "Completed",
            )
            output_folder_path.set(str(output_path.parent))
            set_open_output_button_enabled(True)
            write_export_success_log(process, completed_job)
            message = f"Saved to:\n{output_path}"
            if process.software_encoder_preferred:
                message += "\nSoftware encoder was preferred for this session."
            elif process.fallback_used:
                message += "\nSoftware encoder fallback was used."
            export_message.set(message)
            add_recent_export(completed_job)
            if app_settings.open_output_folder_after_export:
                open_folder(str(output_path.parent))
        else:
            set_open_output_button_enabled(False)
            stdout, stderr = process.communicate()
            log_path = write_export_failure_log(process, job, stdout, stderr)
            export_status.set("Failed")
            export_message.set("Export failed.\nSee the generated log for details.")
            if log_path:
                log_folder_path.set(str(log_path.parent))
                set_open_log_button_enabled(True)
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

    def open_settings_window() -> None:
        create_settings_window(on_saved=reload_settings)

    def open_about_window() -> None:
        create_about_window()

    canvas = tk.Canvas(
        window,
        bg=BACKGROUND,
        borderwidth=0,
        highlightthickness=0,
    )
    scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    content_frame = tk.Frame(canvas, bg=BACKGROUND)
    content_window = canvas.create_window((0, 0), window=content_frame, anchor=tk.N)

    def update_scroll_region(_event=None) -> None:
        canvas.configure(scrollregion=canvas.bbox(tk.ALL))

    def resize_content(event) -> None:
        content_width = min(event.width, 860)
        canvas.itemconfigure(content_window, width=content_width)
        canvas.coords(content_window, event.width // 2, 0)

    def handle_mousewheel(event) -> None:
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    content_frame.bind("<Configure>", update_scroll_region)
    canvas.bind("<Configure>", resize_content)
    canvas.bind_all("<MouseWheel>", handle_mousewheel)

    register_drop_target(window)
    register_drop_target(canvas)
    register_drop_target(content_frame)
    build_header(
        content_frame,
        logo_file=ROOT_DIR / "assets" / "branding" / "eck-icon.png",
        on_settings=open_settings_window,
        on_about=open_about_window,
    )

    build_media_card(
        content_frame,
        selected_file_name=selected_file_name,
        media_info_text=media_info_text,
        on_choose_video=choose_video,
        register_drop_target=register_drop_target,
    )

    center_columns = tk.Frame(content_frame, bg=BACKGROUND)
    center_columns.pack(fill=tk.X, padx=2, pady=(6, 0))
    center_columns.grid_columnconfigure(0, weight=1, uniform="main")
    center_columns.grid_columnconfigure(1, weight=1, uniform="main")

    export_column = tk.Frame(center_columns, bg=BACKGROUND)
    status_column = tk.Frame(center_columns, bg=BACKGROUND)
    export_column.grid(row=0, column=0, sticky="nsew")
    status_column.grid(row=0, column=1, sticky="nsew")

    export_widgets = build_export_card(
        export_column,
        on_export_x=lambda: export_selected("export_to_x.py"),
        on_export_youtube=lambda: export_selected("export_to_youtube.py"),
    )
    x_button = export_widgets["x_button"]
    youtube_button = export_widgets["youtube_button"]

    status_widgets = build_status_card(
        status_column,
        export_status=export_status,
        export_message=export_message,
        on_open_output_folder=open_output_folder,
        on_open_log_folder=open_log_folder,
    )
    progress_bar = status_widgets["progress_bar"]
    open_output_button = status_widgets["open_output_button"]
    open_log_button = status_widgets["open_log_button"]

    build_recent_exports_card(
        content_frame,
        recent_exports_text=recent_exports_text,
    )

    return window


def main() -> None:
    """Run the prototype window."""
    create_window().mainloop()


if __name__ == "__main__":
    main()
