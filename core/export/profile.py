"""Shared export profile model."""

from dataclasses import dataclass


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
    def x(cls) -> "ExportProfile":
        """Return the X export profile."""
        return cls(
            video_codec="h264_nvenc",
            audio_codec="aac",
            preset="p5",
            quality="23",
            audio_bitrate="128k",
            faststart=True,
            pixel_format="yuv420p",
        )

    @classmethod
    def youtube(cls) -> "ExportProfile":
        """Return the YouTube export profile."""
        return cls(
            video_codec="h264_nvenc",
            audio_codec="aac",
            preset="p5",
            quality="18",
            audio_bitrate="320k",
            faststart=True,
            pixel_format="yuv420p",
        )
