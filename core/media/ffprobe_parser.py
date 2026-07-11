"""Parser for ffprobe JSON output."""

import json
from pathlib import Path

from core.media.info import MediaInfo


class FFprobeParseError(RuntimeError):
    """Raised when ffprobe JSON cannot be converted into MediaInfo."""


class FFprobeParser:
    """Convert raw ffprobe JSON into MediaInfo."""

    def parse(self, raw_json: str) -> MediaInfo:
        """Return MediaInfo parsed from raw ffprobe JSON."""
        try:
            data = self._load_json(raw_json)
            streams = self._as_list(data.get("streams"), "streams")
            video = self._find_stream(streams, "video")
            audio = self._find_stream(streams, "audio")
            format_info = self._as_dict(data.get("format"), "format")

            if not video:
                raise FFprobeParseError("Invalid video file: video stream was not found.")

            duration_seconds = self._to_float(format_info.get("duration"))
            file_size_bytes = self._to_int(format_info.get("size"))
            file_name = self._to_string(format_info.get("filename"))

            return MediaInfo(
                file_name=file_name,
                extension=Path(file_name).suffix,
                duration_seconds=duration_seconds,
                duration_text=self._format_duration(duration_seconds),
                file_size_bytes=file_size_bytes,
                file_size_mb=file_size_bytes / 1024 / 1024 if file_size_bytes else 0.0,
                width=self._to_int(video.get("width")),
                height=self._to_int(video.get("height")),
                fps=self._parse_fps(video.get("avg_frame_rate")),
                video_codec=self._to_string(video.get("codec_name")),
                audio_codec=self._to_string(audio.get("codec_name")),
                video_bitrate=self._to_int(video.get("bit_rate")),
                audio_bitrate=self._to_int(audio.get("bit_rate")),
                total_bitrate=self._to_int(format_info.get("bit_rate")),
            )
        except FFprobeParseError:
            raise
        except (ValueError, TypeError, KeyError, IndexError) as exc:
            raise FFprobeParseError("Invalid ffprobe data.") from exc

    def _find_stream(self, streams: list[dict], codec_type: str) -> dict:
        for stream in streams:
            if isinstance(stream, dict) and stream.get("codec_type") == codec_type:
                return stream
        return {}

    def _load_json(self, raw_json: str) -> dict:
        if not isinstance(raw_json, str) or not raw_json.strip():
            raise FFprobeParseError("ffprobe returned empty data.")

        try:
            data = json.loads(raw_json)
        except json.JSONDecodeError as exc:
            raise FFprobeParseError("ffprobe returned invalid JSON.") from exc

        if not isinstance(data, dict):
            raise FFprobeParseError("ffprobe JSON root must be an object.")

        return data

    def _as_list(self, value: object, name: str) -> list:
        if value is None:
            return []
        if not isinstance(value, list):
            raise FFprobeParseError(f"ffprobe field is invalid: {name}.")
        return value

    def _as_dict(self, value: object, name: str) -> dict:
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise FFprobeParseError(f"ffprobe field is invalid: {name}.")
        return value

    def _to_int(self, value: object) -> int:
        if value in (None, ""):
            return 0

        try:
            return int(float(value))
        except (TypeError, ValueError):
            return 0

    def _to_float(self, value: object) -> float:
        if value in (None, ""):
            return 0.0

        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def _to_string(self, value: object) -> str:
        if value is None:
            return ""

        return str(value)

    def _parse_fps(self, value: object) -> float:
        if not isinstance(value, str) or "/" not in value:
            return self._to_float(value)

        numerator, denominator = value.split("/", 1)
        denominator_value = self._to_float(denominator)
        if denominator_value == 0.0:
            return 0.0
        return self._to_float(numerator) / denominator_value

    def _format_duration(self, duration_seconds: float) -> str:
        total_seconds = max(0, int(round(duration_seconds)))
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        if hours > 0:
            return f"{hours} hr {minutes:02d} min"

        if minutes > 0:
            return f"{minutes} min {seconds:02d} sec"

        return f"{seconds} sec"
