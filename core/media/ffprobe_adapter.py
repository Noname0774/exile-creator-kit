"""Adapter for running ffprobe."""

import subprocess


class FFprobeAdapter:
    """Run ffprobe and return raw JSON output."""

    def probe(self, file_path: str) -> str:
        """Return raw ffprobe JSON output."""
        command = [
            "ffprobe",
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            file_path,
        ]

        try:
            result = subprocess.run(command, capture_output=True, text=True)
        except FileNotFoundError as exc:
            raise RuntimeError("ffprobe was not found.") from exc

        if result.returncode != 0:
            message = result.stderr.strip() or "ffprobe failed."
            raise RuntimeError(message)

        return result.stdout

