"""Settings validation."""

from core.settings.model import AppSettings


class SettingsValidator:
    VALID_EXPORT_TARGETS = {"X", "YouTube"}

    def validate(self, settings: AppSettings) -> None:
        if settings.default_export_target not in self.VALID_EXPORT_TARGETS:
            raise ValueError("Invalid default export target.")
