"""Media inspection skeleton."""

from pathlib import Path

from core.media.ffprobe_adapter import FFprobeAdapter
from core.media.ffprobe_parser import FFprobeParser
from core.media.info import MediaInfo


class MediaInspectionError(RuntimeError):
    """Raised when a media file cannot be inspected safely."""


class MediaInspector:
    """Analyze media files and expose metadata."""

    def analyze(self, file_path: str | Path) -> MediaInfo:
        """Analyze a media file and return parsed metadata."""
        path = Path(file_path)
        if not str(path).strip():
            raise MediaInspectionError("Invalid video file: path is empty.")
        if not path.exists():
            raise MediaInspectionError(f"Invalid video file: file does not exist: {path}")
        if not path.is_file():
            raise MediaInspectionError(f"Invalid video file: path is not a file: {path}")

        try:
            raw_json = FFprobeAdapter().probe(str(path))
            return FFprobeParser().parse(raw_json)
        except MediaInspectionError:
            raise
        except RuntimeError as exc:
            raise MediaInspectionError(str(exc)) from exc
        except (ValueError, TypeError, KeyError, IndexError) as exc:
            raise MediaInspectionError("Media inspection failed unexpectedly.") from exc
