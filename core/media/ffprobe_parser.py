"""Parser for ffprobe JSON output."""

import json

from core.media.info import MediaInfo


class FFprobeParser:
    """Convert raw ffprobe JSON into MediaInfo."""

    def parse(self, raw_json: str) -> MediaInfo:
        """Return MediaInfo parsed from raw ffprobe JSON."""
        data = json.loads(raw_json)
        streams = data.get("streams", [])
        video = self._find_stream(streams, "video")
        audio = self._find_stream(streams, "audio")
        format_info = data.get("format", {})

        duration_seconds = self._to_float(format_info.get("duration"))
        file_size_bytes = self._to_int(format_info.get("size"))

        return MediaInfo(
            file_name=format_info.get("filename", ""),
            extension="",
            duration_seconds=duration_seconds,
            duration_text="",
            file_size_bytes=file_size_bytes,
            file_size_mb=file_size_bytes / 1024 / 1024 if file_size_bytes else 0.0,
            width=self._to_int(video.get("width")),
            height=self._to_int(video.get("height")),
            fps=self._parse_fps(video.get("avg_frame_rate")),
            video_codec=video.get("codec_name", ""),
            audio_codec=audio.get("codec_name", ""),
            video_bitrate=self._to_int(video.get("bit_rate")),
            audio_bitrate=self._to_int(audio.get("bit_rate")),
            total_bitrate=self._to_int(format_info.get("bit_rate")),
        )

    def _find_stream(self, streams: list[dict], codec_type: str) -> dict:
        for stream in streams:
            if stream.get("codec_type") == codec_type:
                return stream
        return {}

    def _to_int(self, value: object) -> int:
        return int(value) if value not in (None, "") else 0

    def _to_float(self, value: object) -> float:
        return float(value) if value not in (None, "") else 0.0

    def _parse_fps(self, value: object) -> float:
        if not isinstance(value, str) or "/" not in value:
            return self._to_float(value)

        numerator, denominator = value.split("/", 1)
        denominator_value = self._to_float(denominator)
        if denominator_value == 0.0:
            return 0.0
        return self._to_float(numerator) / denominator_value

