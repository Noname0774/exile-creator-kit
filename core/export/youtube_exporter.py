"""YouTube export command builder."""

from core.export.generic_exporter import GenericExporter
from core.export.profile import ExportProfile


class YouTubeExporter:
    """Build FFmpeg commands for YouTube export."""

    def __init__(self) -> None:
        self._exporter = GenericExporter(ExportProfile.youtube())

    def export(self, input_path: str, output_path: str) -> str:
        """Return the FFmpeg command for a future YouTube export."""
        return self._exporter.export(input_path, output_path)

    def execute(self, input_path: str, output_path: str) -> str:
        """Execute the FFmpeg command and return the output path."""
        return self._exporter.execute(input_path, output_path)
