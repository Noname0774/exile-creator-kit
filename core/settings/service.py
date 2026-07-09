"""Settings service."""

import logging
import subprocess
from dataclasses import replace
from pathlib import Path

from core.settings.defaults import default_settings
from core.settings.model import AppSettings
from core.settings.repository import SettingsRepository
from core.settings.validator import SettingsValidator

logger = logging.getLogger(__name__)


class SettingsService:
    def __init__(
        self,
        repository: SettingsRepository | None = None,
        validator: SettingsValidator | None = None,
    ) -> None:
        self._repository = repository or SettingsRepository()
        self._validator = validator or SettingsValidator()

    def load(self) -> AppSettings:
        settings = self._repository.load()
        try:
            self._validator.validate(settings)
        except ValueError:
            logger.warning("Invalid settings values. Using defaults.", exc_info=True)
            return default_settings()

        return settings

    def save(self, settings: AppSettings) -> None:
        self._validator.validate(settings)
        self._repository.save(settings)

    def get_settings(self) -> AppSettings:
        return self.load()

    def update_settings(self, **changes: object) -> AppSettings:
        settings = replace(self.load(), **changes)
        self.save(settings)
        return settings

    def get_ffmpeg_path(self) -> str:
        executable_path = self._resolve_executable_path(self.load().ffmpeg_path, "ffmpeg")
        self._require_executable(executable_path, "FFmpeg")
        return executable_path

    def get_ffprobe_path(self) -> str:
        executable_path = self._resolve_executable_path(
            self.load().ffprobe_path,
            "ffprobe",
        )
        self._require_executable(executable_path, "FFprobe")
        return executable_path

    def is_ffmpeg_available(self) -> bool:
        executable_path = self._resolve_executable_path(self.load().ffmpeg_path, "ffmpeg")
        return self._is_executable_available(executable_path)

    def is_ffprobe_available(self) -> bool:
        executable_path = self._resolve_executable_path(
            self.load().ffprobe_path,
            "ffprobe",
        )
        return self._is_executable_available(executable_path)

    def get_export_profile_overrides(self, target: str) -> dict[str, object]:
        settings = self.load()
        prefix = target.lower()
        fields = (
            "smart_bitrate",
            "video_codec",
            "audio_codec",
            "preset",
            "quality",
            "audio_bitrate",
            "faststart",
            "pixel_format",
        )
        overrides: dict[str, object] = {}

        for field in fields:
            setting_name = f"{prefix}_{field}"
            if hasattr(settings, setting_name):
                value = getattr(settings, setting_name)
                if value not in ("", None):
                    overrides[field] = value

        return overrides

    def _resolve_executable_path(self, configured_path: str, default_name: str) -> str:
        if not configured_path:
            return default_name

        path_text = configured_path.strip()
        if not path_text:
            return default_name

        path = Path(path_text)
        looks_like_file_path = path.is_absolute() or "\\" in path_text or "/" in path_text
        if looks_like_file_path and not path.exists():
            logger.warning(
                "Configured executable path does not exist: %s. Using default: %s.",
                path_text,
                default_name,
            )
            return default_name

        return path_text

    def _require_executable(self, executable_path: str, display_name: str) -> None:
        if self._is_executable_available(executable_path):
            return

        executable_name = display_name.upper() if display_name == "FFmpeg" else display_name
        raise RuntimeError(
            f"{display_name} was not found.\n"
            f"Please install {executable_name} or update the configured path."
        )

    def _is_executable_available(self, executable_path: str) -> bool:
        try:
            result = subprocess.run(
                [executable_path, "-version"],
                capture_output=True,
                text=True,
            )
        except OSError:
            return False

        return result.returncode == 0
