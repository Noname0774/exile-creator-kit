"""Preflight checks before export."""

from dataclasses import dataclass
from pathlib import Path
import re
import shutil

from core.media.media_summary import MediaSummary
from core.system.encoder_selector import EncoderSelector
from core.system.environment import EnvironmentInfo


@dataclass(frozen=True)
class PreflightCheckItem:
    """Single preflight check result."""

    name: str
    status: str
    message: str


@dataclass(frozen=True)
class PreflightResult:
    """Complete preflight result for future Status Card display."""

    status: str
    items: tuple[PreflightCheckItem, ...]


class PreflightChecker:
    """Validate export readiness without starting an export."""

    OK = "OK"
    WARNING = "Warning"
    ERROR = "Error"

    def __init__(self, encoder_selector: EncoderSelector | None = None) -> None:
        self._encoder_selector = encoder_selector or EncoderSelector()

    def check(
        self,
        environment_info: EnvironmentInfo,
        media_summary: MediaSummary,
        *,
        input_file: str | Path | None = None,
        output_folder: str | Path | None = None,
    ) -> PreflightResult:
        """Return export readiness checks for a media summary."""
        items = (
            self._gpu(environment_info),
            self._encoder(environment_info),
            self._ffmpeg(environment_info),
            self._ffprobe(environment_info),
            self._input_file(input_file, media_summary),
            self._output_folder(output_folder),
            self._disk_space(output_folder, media_summary),
            self._estimated_export_time(environment_info, media_summary),
            self._estimated_export_size(media_summary),
        )
        return PreflightResult(status=self._overall_status(items), items=items)

    def _gpu(self, environment_info: EnvironmentInfo) -> PreflightCheckItem:
        if environment_info.gpu_vendor == "Unknown":
            return PreflightCheckItem(
                name="GPU",
                status=self.WARNING,
                message="GPU could not be identified. Software export remains available.",
            )

        return PreflightCheckItem(
            name="GPU",
            status=self.OK,
            message=f"{environment_info.gpu_vendor}: {environment_info.gpu_name}",
        )

    def _encoder(self, environment_info: EnvironmentInfo) -> PreflightCheckItem:
        decision = self._encoder_selector.select(environment_info)
        if decision.selected_encoder == "Software (libx264)":
            return PreflightCheckItem(
                name="Encoder",
                status=self.WARNING,
                message=decision.reason,
            )

        return PreflightCheckItem(
            name="Encoder",
            status=self.OK,
            message=f"{decision.auto_label} selected.",
        )

    def _ffmpeg(self, environment_info: EnvironmentInfo) -> PreflightCheckItem:
        if environment_info.ffmpeg_version == "Unknown":
            return PreflightCheckItem(
                name="FFmpeg",
                status=self.ERROR,
                message="FFmpeg was not found or could not be executed.",
            )

        return PreflightCheckItem(
            name="FFmpeg",
            status=self.OK,
            message="FFmpeg is available.",
        )

    def _ffprobe(self, environment_info: EnvironmentInfo) -> PreflightCheckItem:
        if environment_info.ffprobe_version == "Unknown":
            return PreflightCheckItem(
                name="FFprobe",
                status=self.ERROR,
                message="FFprobe was not found or could not be executed.",
            )

        return PreflightCheckItem(
            name="FFprobe",
            status=self.OK,
            message="FFprobe is available.",
        )

    def _input_file(
        self,
        input_file: str | Path | None,
        media_summary: MediaSummary,
    ) -> PreflightCheckItem:
        if input_file is None:
            if media_summary.filename:
                return PreflightCheckItem(
                    name="Input File",
                    status=self.OK,
                    message=f"Media summary loaded: {media_summary.filename}",
                )

            return PreflightCheckItem(
                name="Input File",
                status=self.WARNING,
                message="Input file path was not provided for preflight.",
            )

        path = Path(input_file)
        if not path.exists():
            return PreflightCheckItem(
                name="Input File",
                status=self.ERROR,
                message=f"Input file does not exist: {path}",
            )

        if not path.is_file():
            return PreflightCheckItem(
                name="Input File",
                status=self.ERROR,
                message=f"Input path is not a file: {path}",
            )

        return PreflightCheckItem(
            name="Input File",
            status=self.OK,
            message=f"Input file is available: {path.name}",
        )

    def _output_folder(self, output_folder: str | Path | None) -> PreflightCheckItem:
        if output_folder is None:
            return PreflightCheckItem(
                name="Output Folder",
                status=self.WARNING,
                message="Output folder was not provided for preflight.",
            )

        path = Path(output_folder)
        if not path.exists():
            return PreflightCheckItem(
                name="Output Folder",
                status=self.ERROR,
                message=f"Output folder does not exist: {path}",
            )

        if not path.is_dir():
            return PreflightCheckItem(
                name="Output Folder",
                status=self.ERROR,
                message=f"Output path is not a folder: {path}",
            )

        return PreflightCheckItem(
            name="Output Folder",
            status=self.OK,
            message=f"Output folder is available: {path}",
        )

    def _disk_space(
        self,
        output_folder: str | Path | None,
        media_summary: MediaSummary,
    ) -> PreflightCheckItem:
        required_bytes = max(
            self._parse_size(media_summary.estimated_x_export_size),
            self._parse_size(media_summary.estimated_youtube_export_size),
        )
        if output_folder is None or required_bytes <= 0:
            return PreflightCheckItem(
                name="Disk Space",
                status=self.WARNING,
                message="Disk space could not be fully checked.",
            )

        path = Path(output_folder)
        if not path.exists():
            return PreflightCheckItem(
                name="Disk Space",
                status=self.ERROR,
                message="Disk space could not be checked because the output folder is missing.",
            )

        free_bytes = shutil.disk_usage(path).free
        if free_bytes < required_bytes:
            return PreflightCheckItem(
                name="Disk Space",
                status=self.ERROR,
                message=(
                    f"Not enough free space. Required about "
                    f"{self._format_size(required_bytes)}."
                ),
            )

        return PreflightCheckItem(
            name="Disk Space",
            status=self.OK,
            message=f"Free space is sufficient: {self._format_size(free_bytes)} available.",
        )

    def _estimated_export_time(
        self,
        environment_info: EnvironmentInfo,
        media_summary: MediaSummary,
    ) -> PreflightCheckItem:
        duration_seconds = self._parse_duration(media_summary.duration)
        if duration_seconds <= 0:
            return PreflightCheckItem(
                name="Estimated Export Time",
                status=self.WARNING,
                message="Export time could not be estimated.",
            )

        decision = self._encoder_selector.select(environment_info)
        speed_factor = 0.6 if decision.selected_encoder != "Software (libx264)" else 1.4
        estimated_seconds = max(1, int(duration_seconds * speed_factor))
        return PreflightCheckItem(
            name="Estimated Export Time",
            status=self.OK,
            message=f"Estimated export time: {self._format_duration(estimated_seconds)}.",
        )

    def _estimated_export_size(self, media_summary: MediaSummary) -> PreflightCheckItem:
        return PreflightCheckItem(
            name="Estimated Export Size",
            status=self.OK,
            message=(
                f"X: {media_summary.estimated_x_export_size}; "
                f"YouTube: {media_summary.estimated_youtube_export_size}"
            ),
        )

    def _overall_status(self, items: tuple[PreflightCheckItem, ...]) -> str:
        statuses = {item.status for item in items}
        if self.ERROR in statuses:
            return self.ERROR
        if self.WARNING in statuses:
            return self.WARNING
        return self.OK

    def _parse_size(self, value: str) -> int:
        match = re.search(r"([\d.]+)\s*(GB|MB|KB)", value, re.IGNORECASE)
        if not match:
            return 0

        amount = float(match.group(1))
        unit = match.group(2).lower()
        multipliers = {"kb": 1024, "mb": 1024**2, "gb": 1024**3}
        return int(amount * multipliers[unit])

    def _parse_duration(self, value: str) -> int:
        hours = self._match_duration_part(value, "hr")
        minutes = self._match_duration_part(value, "min")
        seconds = self._match_duration_part(value, "sec")
        return hours * 3600 + minutes * 60 + seconds

    def _match_duration_part(self, value: str, unit: str) -> int:
        match = re.search(rf"(\d+)\s*{unit}", value, re.IGNORECASE)
        return int(match.group(1)) if match else 0

    def _format_size(self, size_bytes: int) -> str:
        size_mb = size_bytes / (1024 * 1024)
        if size_mb >= 1024:
            return f"{size_mb / 1024:.2f} GB"

        return f"{size_mb:.2f} MB"

    def _format_duration(self, seconds: int) -> str:
        if seconds >= 3600:
            return f"{seconds // 3600} hr {(seconds % 3600) // 60:02d} min"
        if seconds >= 60:
            return f"{seconds // 60} min {seconds % 60:02d} sec"
        return f"{seconds} sec"
