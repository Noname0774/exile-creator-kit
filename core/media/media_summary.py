"""Premium UI media summary model."""

from dataclasses import dataclass
from pathlib import Path

from core.media.info import MediaInfo
from core.media.inspector import MediaInspector
from core.media.smart_bitrate import SmartBitrate


@dataclass(frozen=True)
class MediaSummary:
    """Display-ready media details for future UI cards."""

    filename: str
    resolution: str
    fps: float
    duration: str
    filesize: str
    video_codec: str
    audio_codec: str
    video_bitrate: str
    audio_bitrate: str
    container: str
    estimated_x_export_size: str
    estimated_youtube_export_size: str

    @classmethod
    def from_file(cls, file_path: str | Path) -> "MediaSummary":
        """Analyze a media file and return a display-ready summary."""
        media_info = MediaInspector().analyze(file_path)
        return cls.from_media_info(media_info)

    @classmethod
    def from_media_info(cls, media_info: MediaInfo) -> "MediaSummary":
        """Build a display-ready summary from analyzed media info."""
        return cls(
            filename=media_info.file_name,
            resolution=cls._resolution(media_info),
            fps=media_info.fps,
            duration=media_info.duration_text,
            filesize=cls._format_size(media_info.file_size_bytes),
            video_codec=media_info.video_codec,
            audio_codec=media_info.audio_codec,
            video_bitrate=cls._format_bitrate(media_info.video_bitrate),
            audio_bitrate=cls._format_bitrate(media_info.audio_bitrate),
            container=cls._container(media_info),
            estimated_x_export_size=cls._estimate_x_size(media_info),
            estimated_youtube_export_size=cls._estimate_youtube_size(media_info),
        )

    @staticmethod
    def _resolution(media_info: MediaInfo) -> str:
        if media_info.width <= 0 or media_info.height <= 0:
            return "Unknown"

        return f"{media_info.width} x {media_info.height}"

    @staticmethod
    def _container(media_info: MediaInfo) -> str:
        extension = media_info.extension.strip().lstrip(".")
        return extension.upper() if extension else "Unknown"

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        if size_bytes <= 0:
            return "Unknown"

        size_mb = size_bytes / (1024 * 1024)
        if size_mb >= 1024:
            return f"{size_mb / 1024:.2f} GB"

        return f"{size_mb:.2f} MB"

    @staticmethod
    def _format_bitrate(bitrate: int) -> str:
        if bitrate <= 0:
            return "Unknown"

        if bitrate >= 1_000_000:
            return f"{bitrate / 1_000_000:.2f} Mbps"

        return f"{bitrate / 1_000:.0f} Kbps"

    @classmethod
    def _estimate_x_size(cls, media_info: MediaInfo) -> str:
        video_bitrate = SmartBitrate().calculate(media_info.duration_seconds)
        total_bitrate = video_bitrate + SmartBitrate.RESERVED_AUDIO_BITRATE
        return cls._estimate_size(media_info.duration_seconds, total_bitrate)

    @classmethod
    def _estimate_youtube_size(cls, media_info: MediaInfo) -> str:
        source_bitrate = media_info.total_bitrate
        if source_bitrate <= 0:
            source_bitrate = media_info.video_bitrate + media_info.audio_bitrate

        return cls._estimate_size(media_info.duration_seconds, source_bitrate)

    @classmethod
    def _estimate_size(cls, duration_seconds: float, total_bitrate: int) -> str:
        if duration_seconds <= 0 or total_bitrate <= 0:
            return "Unknown"

        estimated_bytes = int((total_bitrate * duration_seconds) / 8)
        return cls._format_size(estimated_bytes)
