"""Media metadata models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class MediaInfo:
    """Immutable analyzed media metadata."""

    file_name: str
    extension: str
    duration_seconds: float
    duration_text: str
    file_size_bytes: int
    file_size_mb: float
    width: int
    height: int
    fps: float
    video_codec: str
    audio_codec: str
    video_bitrate: int
    audio_bitrate: int
    total_bitrate: int

    @classmethod
    def empty(cls) -> "MediaInfo":
        """Return an empty MediaInfo instance."""
        return cls(
            file_name="",
            extension="",
            duration_seconds=0.0,
            duration_text="",
            file_size_bytes=0,
            file_size_mb=0.0,
            width=0,
            height=0,
            fps=0.0,
            video_codec="",
            audio_codec="",
            video_bitrate=0,
            audio_bitrate=0,
            total_bitrate=0,
        )
