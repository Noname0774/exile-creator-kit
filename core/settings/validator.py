"""Settings validation."""

from core.settings.model import AppSettings


class SettingsValidator:
    VALID_EXPORT_TARGETS = {"X", "YouTube"}

    def validate(self, settings: AppSettings) -> None:
        if settings.default_export_target not in self.VALID_EXPORT_TARGETS:
            raise ValueError("Invalid default export target.")

        if not isinstance(settings.remember_last_selected_folder, bool):
            raise ValueError("Remember last selected folder must be a boolean.")

        if not isinstance(settings.open_output_folder_after_export, bool):
            raise ValueError("Open output folder after export must be a boolean.")
