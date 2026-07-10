"""Environment diagnostics for user-facing status checks."""

from dataclasses import dataclass
import os
from pathlib import Path

from core.system.encoder_selector import EncoderSelector
from core.system.environment import EnvironmentInfo


@dataclass(frozen=True)
class DiagnosticItem:
    """Single user-facing diagnostic result."""

    name: str
    status: str
    message: str


class EnvironmentDiagnostics:
    """Generate reusable diagnostics from detected environment information."""

    OK = "OK"
    WARNING = "Warning"
    ERROR = "Error"

    def __init__(self, encoder_selector: EncoderSelector | None = None) -> None:
        self._encoder_selector = encoder_selector or EncoderSelector()

    def diagnose(
        self,
        environment_info: EnvironmentInfo,
        output_folder: str | None = None,
    ) -> list[DiagnosticItem]:
        """Return diagnostics suitable for future Settings/About display."""
        return [
            self._gpu(environment_info),
            self._encoder(environment_info),
            self._ffmpeg(environment_info),
            self._ffprobe(environment_info),
            self._output_folder(output_folder),
            self._app_version(environment_info),
        ]

    def _gpu(self, environment_info: EnvironmentInfo) -> DiagnosticItem:
        if (
            environment_info.gpu_vendor == "Unknown"
            or environment_info.gpu_name == "Unknown"
        ):
            return DiagnosticItem(
                name="GPU",
                status=self.WARNING,
                message="GPU could not be identified. Software encoding is available.",
            )

        return DiagnosticItem(
            name="GPU",
            status=self.OK,
            message=f"{environment_info.gpu_vendor}: {environment_info.gpu_name}",
        )

    def _encoder(self, environment_info: EnvironmentInfo) -> DiagnosticItem:
        decision = self._encoder_selector.select(environment_info)
        if decision.selected_encoder == "Software (libx264)":
            return DiagnosticItem(
                name="Encoder",
                status=self.WARNING,
                message=decision.reason,
            )

        return DiagnosticItem(
            name="Encoder",
            status=self.OK,
            message=f"{decision.auto_label} selected. {decision.reason}",
        )

    def _ffmpeg(self, environment_info: EnvironmentInfo) -> DiagnosticItem:
        if environment_info.ffmpeg_version == "Unknown":
            return DiagnosticItem(
                name="FFmpeg",
                status=self.ERROR,
                message="FFmpeg was not found or could not be executed.",
            )

        return DiagnosticItem(
            name="FFmpeg",
            status=self.OK,
            message=environment_info.ffmpeg_version,
        )

    def _ffprobe(self, environment_info: EnvironmentInfo) -> DiagnosticItem:
        if environment_info.ffprobe_version == "Unknown":
            return DiagnosticItem(
                name="FFprobe",
                status=self.ERROR,
                message="FFprobe was not found or could not be executed.",
            )

        return DiagnosticItem(
            name="FFprobe",
            status=self.OK,
            message=environment_info.ffprobe_version,
        )

    def _output_folder(self, output_folder: str | None) -> DiagnosticItem:
        if not output_folder:
            return DiagnosticItem(
                name="Output Folder",
                status=self.WARNING,
                message="Output folder was not provided for diagnostics.",
            )

        path = Path(output_folder)
        if not path.exists():
            return DiagnosticItem(
                name="Output Folder",
                status=self.ERROR,
                message=f"Output folder does not exist: {path}",
            )

        if not os.access(path, os.W_OK):
            return DiagnosticItem(
                name="Output Folder",
                status=self.ERROR,
                message=f"Output folder is not writable: {path}",
            )

        return DiagnosticItem(
            name="Output Folder",
            status=self.OK,
            message=f"Output folder is writable: {path}",
        )

    def _app_version(self, environment_info: EnvironmentInfo) -> DiagnosticItem:
        if environment_info.app_version == "Unknown":
            return DiagnosticItem(
                name="App Version",
                status=self.WARNING,
                message="Application version could not be read.",
            )

        return DiagnosticItem(
            name="App Version",
            status=self.OK,
            message=environment_info.app_version,
        )
