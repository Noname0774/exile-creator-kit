"""Settings JSON repository."""

import json
import logging
from dataclasses import asdict
from pathlib import Path

from core.settings.defaults import default_settings
from core.settings.model import AppSettings
from core.storage.path_resolver import app_data_file, migrate_legacy_json_file

logger = logging.getLogger(__name__)


class SettingsRepository:
    def __init__(self, file_path: str | Path | None = None) -> None:
        if file_path is None:
            self._file_path = app_data_file("settings.json")
            migrate_legacy_json_file(self._file_path, "settings.json", dict)
        else:
            self._file_path = Path(file_path)

    def load(self) -> AppSettings:
        defaults = default_settings()
        if self._file_path is None:
            logger.warning("Settings storage unavailable. Using defaults.")
            return defaults

        if not self._file_path.exists():
            return defaults

        try:
            with self._file_path.open("r", encoding="utf-8") as settings_file:
                data = json.load(settings_file)
        except (OSError, json.JSONDecodeError):
            logger.warning("Failed to load settings. Using defaults.", exc_info=True)
            return defaults

        if not isinstance(data, dict):
            logger.warning("Settings file is not a JSON object. Using defaults.")
            return defaults

        merged_data = asdict(defaults)
        merged_data.update(
            {key: value for key, value in data.items() if key in merged_data}
        )
        return AppSettings(**merged_data)

    def save(self, settings: AppSettings) -> None:
        if self._file_path is None:
            logger.warning("Settings storage unavailable. Save skipped.")
            return

        try:
            self._file_path.parent.mkdir(parents=True, exist_ok=True)
            with self._file_path.open("w", encoding="utf-8") as settings_file:
                json.dump(asdict(settings), settings_file, indent=2)
        except OSError:
            logger.warning("Failed to save settings.", exc_info=True)
