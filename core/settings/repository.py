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
        defaults = default_settings()
        if not self._file_path.exists():
            return defaults

        with self._file_path.open("r", encoding="utf-8") as settings_file:
            data = json.load(settings_file)

        merged_data = asdict(defaults)
        merged_data.update(
            {key: value for key, value in data.items() if key in merged_data}
        )
        return AppSettings(**merged_data)

    def save(self, settings: AppSettings) -> None:
        with self._file_path.open("w", encoding="utf-8") as settings_file:
            json.dump(asdict(settings), settings_file, indent=2)
