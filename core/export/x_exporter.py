"""X (Twitter) export command builder."""

from core.export.generic_exporter import GenericExporter
from core.export.profile import ExportProfile


class XExporter:
    """Build FFmpeg commands for X export."""

    def __init__(self) -> None:
        self._exporter = GenericExporter(ExportProfile.x())

    def export(
        self,
        input_path: str,
        output_path: str,
        video_bitrate: int | None = None,
    ) -> str:
        """Return the FFmpeg command for a future X export."""
        return self._exporter.export(input_path, output_path, video_bitrate)

    def execute(
        self,
        input_path: str,
        output_path: str,
        video_bitrate: int | None = None,
    ) -> str:
        """Execute the FFmpeg command and return the output path."""
        return self._exporter.execute(input_path, output_path, video_bitrate)
