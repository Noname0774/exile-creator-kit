"""Settings repository interface."""

from core.settings.defaults import default_settings
from core.settings.model import AppSettings


class SettingsRepository:
    def load(self) -> AppSettings:
        return default_settings()

    def save(self, settings: AppSettings) -> None:
        raise NotImplementedError("Settings persistence will be implemented later.")
