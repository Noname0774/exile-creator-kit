"""Shared export profile model."""

from dataclasses import dataclass

from core.settings.service import SettingsService


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
            },
            settings_service=settings_service,
        )

    @classmethod
    def _from_defaults(
        cls,
        target: str,
        defaults: dict[str, object],
        settings_service: SettingsService | None,
    ) -> "ExportProfile":
        service = settings_service or SettingsService()
        values = defaults | service.get_export_profile_overrides(target)
        return cls(**values)
