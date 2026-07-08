"""Media inspection skeleton."""

from pathlib import Path

from core.media.ffprobe_adapter import FFprobeAdapter
from core.media.ffprobe_parser import FFprobeParser
from core.media.info import MediaInfo


class MediaInspector:
    """Analyze media files and expose metadata."""

    def analyze(self, file_path: str | Path) -> MediaInfo:
        """Analyze a media file and return parsed metadata."""
        raw_json = FFprobeAdapter().probe(str(file_path))
        return FFprobeParser().parse(raw_json)
