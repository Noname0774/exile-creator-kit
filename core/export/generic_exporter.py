"""Generic FFmpeg exporter driven by ExportProfile."""

import subprocess

from core.export.profile import ExportProfile


class GenericExporter:
    """Build and execute FFmpeg commands from an export profile."""

    def __init__(self, profile: ExportProfile) -> None:
        self.profile = profile

    def export(
        self,
        input_path: str,
        output_path: str,
        video_bitrate: int | None = None,
    ) -> str:
        """Return an FFmpeg command built from the export profile."""
        command = [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-c:v",
            self.profile.video_codec,
            "-preset",
            self.profile.preset,
        ]

        if self.profile.quality:
            command.extend(["-cq", self.profile.quality])

        if video_bitrate is not None:
            command.extend(["-b:v", str(video_bitrate)])

        if self.profile.pixel_format:
            command.extend(["-pix_fmt", self.profile.pixel_format])

        command.extend(["-c:a", self.profile.audio_codec])

        if self.profile.audio_bitrate:
            command.extend(["-b:a", self.profile.audio_bitrate])

        if self.profile.faststart:
            command.extend(["-movflags", "+faststart"])

        command.append(output_path)

        return subprocess.list2cmdline(command)

    def execute(
        self,
        input_path: str,
        output_path: str,
        video_bitrate: int | None = None,
    ) -> str:
        """Execute the FFmpeg command and return the output path."""
        command = self.export(input_path, output_path, video_bitrate)
        result = subprocess.run(command, capture_output=True, shell=True, text=True)

        if result.returncode != 0:
            message = result.stderr.strip() or "FFmpeg export failed."
            raise RuntimeError(message)

        return output_path

