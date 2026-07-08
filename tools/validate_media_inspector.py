"""Validate MediaInspector with a local media file."""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from core.media.inspector import MediaInspector  # noqa: E402
from core.media.smart_bitrate import SmartBitrate  # noqa: E402


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python tools/validate_media_inspector.py <media-file>")
        return 1

    media_info = MediaInspector().analyze(sys.argv[1])
    recommended_bitrate = SmartBitrate().calculate(media_info.duration_seconds)

    print("--------------------------------")
    print(f"File: {media_info.file_name}")
    print(f"Duration: {media_info.duration_seconds}")
    print(f"Resolution: {media_info.width}x{media_info.height}")
    print(f"FPS: {media_info.fps}")
    print(f"Video Codec: {media_info.video_codec}")
    print(f"Audio Codec: {media_info.audio_codec}")
    print(f"Current Bitrate: {media_info.total_bitrate}")
    print(f"Recommended Bitrate: {recommended_bitrate}")
    print("--------------------------------")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
