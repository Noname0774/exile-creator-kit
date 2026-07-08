"""Settings service."""

from core.settings.model import AppSettings
from core.settings.repository import SettingsRepository
from core.settings.validator import SettingsValidator


class SettingsService:
    def __init__(
        self,
        repository: SettingsRepository | None = None,
        validator: SettingsValidator | None = None,
    ) -> None:
        self._repository = repository or SettingsRepository()
        self._validator = validator or SettingsValidator()

    def get_settings(self) -> AppSettings:
        settings = self._repository.load()
        self._validator.validate(settings)
        return settings
