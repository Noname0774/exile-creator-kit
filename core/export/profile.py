"""Shared export profile model."""

from dataclasses import dataclass

from core.export.presets import ExportPreset
from core.settings.service import SettingsService

ENCODER_AUTO = "Auto (Recommended)"
ENCODER_NVENC = "NVIDIA NVENC"
ENCODER_SOFTWARE = "Software (libx264)"


@dataclass(frozen=True)
class ExportProfile:
    """Immutable export settings shared by exporters."""

    video_codec: str
    audio_codec: str
    preset: str
    quality: str
    audio_bitrate: str
    faststart: bool
    pixel_format: str
    smart_bitrate: bool = True

    @classmethod
    def x(cls, settings_service: SettingsService | None = None) -> "ExportProfile":
        """Return the X export profile."""
        return cls._from_defaults(
            target="X",
            defaults={
                "video_codec": "h264_nvenc",
                "audio_codec": "aac",
                "preset": "p5",
                "quality": "23",
                "audio_bitrate": "128k",
                "faststart": True,
                "pixel_format": "yuv420p",
                "smart_bitrate": True,
            },
            settings_service=settings_service,
        )

    @classmethod
    def youtube(cls, settings_service: SettingsService | None = None) -> "ExportProfile":
        """Return the YouTube export profile."""
        return cls._from_defaults(
            target="YouTube",
            defaults={
                "video_codec": "h264_nvenc",
                "audio_codec": "aac",
                "preset": "p5",
                "quality": "18",
                "audio_bitrate": "320k",
                "faststart": True,
                "pixel_format": "yuv420p",
                "smart_bitrate": False,
            },
            settings_service=settings_service,
        )

    @classmethod
    def from_preset(
        cls,
        preset: ExportPreset,
        *,
        fallback_target: str = "X",
        settings_service: SettingsService | None = None,
    ) -> "ExportProfile":
        """Return an export profile for a selected preset."""
        if preset.is_custom():
            if fallback_target == "YouTube":
                return cls.youtube(settings_service=settings_service)

            return cls.x(settings_service=settings_service)

        defaults = {
            "video_codec": "h264_nvenc",
            "audio_codec": preset.audio_codec,
            "preset": "p5",
            "quality": "23",
            "audio_bitrate": preset.audio_bitrate,
            "faststart": True,
            "pixel_format": "yuv420p",
            "smart_bitrate": preset.video_bitrate in {"smart", "size aware"},
        }

        if preset.name == "YouTube (High Quality)":
            defaults["quality"] = "18"
            defaults["smart_bitrate"] = False
        elif preset.name == "YouTube Shorts":
            defaults["quality"] = "20"
            defaults["smart_bitrate"] = False
        elif preset.name == "Discord":
            defaults["quality"] = "28"
            defaults["smart_bitrate"] = True

        service = settings_service or SettingsService()
        cls._apply_encoder_setting(defaults, service)
        return cls(**defaults)

    @classmethod
    def _from_defaults(
        cls,
        target: str,
        defaults: dict[str, object],
        settings_service: SettingsService | None,
    ) -> "ExportProfile":
        service = settings_service or SettingsService()
        values = defaults | service.get_export_profile_overrides(target)
        cls._apply_encoder_setting(values, service)
        return cls(**values)

    @staticmethod
    def _apply_encoder_setting(
        values: dict[str, object],
        service: SettingsService,
    ) -> None:
        encoder = service.get_settings().encoder
        if encoder == ENCODER_SOFTWARE:
            values["video_codec"] = "libx264"
            values["preset"] = "medium"
            values["quality"] = ""
            return

        if encoder in {ENCODER_AUTO, ENCODER_NVENC}:
            values["video_codec"] = "h264_nvenc"
