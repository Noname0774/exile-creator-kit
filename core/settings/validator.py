"""Settings validation."""

import logging
import re
from typing import Any

from core.settings.defaults import default_settings
from core.settings.model import AppSettings

logger = logging.getLogger(__name__)


class SettingsValidator:
    VALID_EXPORT_TARGETS = {"X", "YouTube"}
    VALID_ENCODERS = {"Auto (Recommended)", "NVIDIA NVENC", "Software (libx264)"}
    VALID_PRESETS = {"p1", "p2", "p3", "p4", "p5", "p6", "p7"}
    VALID_PIXEL_FORMATS = {"yuv420p", "nv12", "p010le"}
    BITRATE_PATTERN = re.compile(r"^[1-9][0-9]*[kKmM]?$")

    def validate(self, settings: AppSettings) -> None:
        defaults = default_settings()

        self._validate_choice(
            settings,
            "default_export_target",
            settings.default_export_target,
            self.VALID_EXPORT_TARGETS,
            defaults.default_export_target,
        )
        self._validate_choice(
            settings,
            "encoder",
            settings.encoder,
            self.VALID_ENCODERS,
            defaults.encoder,
        )
        self._validate_bool(
            settings,
            "remember_last_selected_folder",
            settings.remember_last_selected_folder,
            defaults.remember_last_selected_folder,
        )
        self._validate_bool(
            settings,
            "open_output_folder_after_export",
            settings.open_output_folder_after_export,
            defaults.open_output_folder_after_export,
        )

        self._validate_bool(
            settings,
            "x_smart_bitrate",
            settings.x_smart_bitrate,
            defaults.x_smart_bitrate,
        )
        self._validate_bitrate(
            settings,
            "x_audio_bitrate",
            settings.x_audio_bitrate,
            defaults.x_audio_bitrate,
        )
        self._validate_choice(
            settings,
            "x_preset",
            settings.x_preset,
            self.VALID_PRESETS,
            defaults.x_preset,
        )
        self._validate_choice(
            settings,
            "x_pixel_format",
            settings.x_pixel_format,
            self.VALID_PIXEL_FORMATS,
            defaults.x_pixel_format,
        )

        self._validate_quality(
            settings,
            "youtube_quality",
            settings.youtube_quality,
            defaults.youtube_quality,
        )
        self._validate_bitrate(
            settings,
            "youtube_audio_bitrate",
            settings.youtube_audio_bitrate,
            defaults.youtube_audio_bitrate,
        )
        self._validate_choice(
            settings,
            "youtube_pixel_format",
            settings.youtube_pixel_format,
            self.VALID_PIXEL_FORMATS,
            defaults.youtube_pixel_format,
        )
        self._validate_bool(
            settings,
            "youtube_faststart",
            settings.youtube_faststart,
            defaults.youtube_faststart,
        )

    def _validate_bool(
        self,
        settings: AppSettings,
        field_name: str,
        value: object,
        default_value: bool,
    ) -> None:
        if isinstance(value, bool):
            return

        self._reject(settings, field_name, value, default_value, "must be a boolean")

    def _validate_bitrate(
        self,
        settings: AppSettings,
        field_name: str,
        value: object,
        default_value: str,
    ) -> None:
        if isinstance(value, str) and self.BITRATE_PATTERN.match(value):
            return

        self._reject(
            settings,
            field_name,
            value,
            default_value,
            "must be a positive bitrate string",
        )

    def _validate_choice(
        self,
        settings: AppSettings,
        field_name: str,
        value: object,
        valid_values: set[str],
        default_value: str,
    ) -> None:
        if isinstance(value, str) and value in valid_values:
            return

        self._reject(settings, field_name, value, default_value, "is not supported")

    def _validate_quality(
        self,
        settings: AppSettings,
        field_name: str,
        value: object,
        default_value: str,
    ) -> None:
        if isinstance(value, str) and value.isdigit() and 0 <= int(value) <= 51:
            return

        self._reject(
            settings,
            field_name,
            value,
            default_value,
            "must be a number from 0 to 51",
        )

    def _reject(
        self,
        settings: AppSettings,
        field_name: str,
        value: object,
        default_value: Any,
        reason: str,
    ) -> None:
        logger.warning(
            "Invalid setting rejected: %s=%r; %s. Using default: %r.",
            field_name,
            value,
            reason,
            default_value,
        )
        object.__setattr__(settings, field_name, default_value)
