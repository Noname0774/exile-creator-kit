"""Adapter for running ffprobe."""

import subprocess

from core.settings.service import SettingsService


class FFprobeAdapter:
    """Run ffprobe and return raw JSON output."""

    def __init__(self, settings_service: SettingsService | None = None) -> None:
        self._settings_service = settings_service or SettingsService()

    def probe(self, file_path: str) -> str:
        """Return raw ffprobe JSON output."""
        command = [
            self._settings_service.get_ffprobe_path(),
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            file_path,
        ]

        try:
            result = subprocess.run(command, capture_output=True, text=True)
        except FileNotFoundError as exc:
            raise RuntimeError("ffprobe was not found.") from exc

        if result.returncode != 0:
            message = result.stderr.strip() or "ffprobe failed."
            raise RuntimeError(message)

        return result.stdout
