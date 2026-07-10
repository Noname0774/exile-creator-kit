"""Application environment detection."""

from dataclasses import dataclass
import platform
import subprocess
from pathlib import Path

from core.settings.service import SettingsService
from core.system.gpu_detector import GPUDetector


@dataclass(frozen=True)
class EnvironmentInfo:
    """Immutable system environment summary."""

    gpu_vendor: str
    gpu_name: str
    available_encoders: tuple[str, ...]
    os_name: str
    python_version: str
    ffmpeg_version: str
    ffprobe_version: str
    app_version: str


class EnvironmentDetector:
    """Collect environment information without changing app behavior."""

    def __init__(
        self,
        gpu_detector: GPUDetector | None = None,
        settings_service: SettingsService | None = None,
    ) -> None:
        self._gpu_detector = gpu_detector or GPUDetector()
        self._settings_service = settings_service or SettingsService()

    def detect(self) -> EnvironmentInfo:
        """Return the current application environment."""
        gpu_vendor, gpu_name, encoders = self._gpu_detector.detect()
        return EnvironmentInfo(
            gpu_vendor=gpu_vendor,
            gpu_name=gpu_name,
            available_encoders=tuple(encoders),
            os_name=platform.platform(),
            python_version=platform.python_version(),
            ffmpeg_version=self._tool_version("ffmpeg"),
            ffprobe_version=self._tool_version("ffprobe"),
            app_version=self._app_version(),
        )

    def _tool_version(self, tool_name: str) -> str:
        try:
            executable = (
                self._settings_service.get_ffmpeg_path()
                if tool_name == "ffmpeg"
                else self._settings_service.get_ffprobe_path()
            )
            result = subprocess.run(
                [executable, "-version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
        except (OSError, RuntimeError, subprocess.TimeoutExpired):
            return "Unknown"

        if result.returncode != 0:
            return "Unknown"

        first_line = result.stdout.splitlines()[0] if result.stdout else ""
        return first_line.strip() or "Unknown"

    def _app_version(self) -> str:
        version_path = Path(__file__).resolve().parents[2] / "VERSION"
        try:
            return version_path.read_text(encoding="utf-8").strip() or "Unknown"
        except OSError:
            return "Unknown"
