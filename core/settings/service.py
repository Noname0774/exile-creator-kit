"""Settings service."""

from dataclasses import replace

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

    def load(self) -> AppSettings:
        settings = self._repository.load()
        self._validator.validate(settings)
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
