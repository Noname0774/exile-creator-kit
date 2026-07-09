"""Settings JSON repository."""

import json
from dataclasses import asdict
from pathlib import Path

from core.settings.defaults import default_settings
from core.settings.model import AppSettings


class SettingsRepository:
    def __init__(self, file_path: str | Path = "settings.json") -> None:
        self._file_path = Path(file_path)

    def load(self) -> AppSettings:
        if not self._file_path.exists():
            return default_settings()

        with self._file_path.open("r", encoding="utf-8") as settings_file:
            data = json.load(settings_file)

        return AppSettings(**data)

    def save(self, settings: AppSettings) -> None:
        with self._file_path.open("w", encoding="utf-8") as settings_file:
            json.dump(asdict(settings), settings_file, indent=2)
