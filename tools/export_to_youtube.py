"""Export a media file for YouTube using the current core pipeline."""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from core.export import YouTubeExporter  # noqa: E402
from core.export.profile import ExportProfile  # noqa: E402
from core.media.inspector import MediaInspector  # noqa: E402


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python tools/export_to_youtube.py <media-file>")
        return 1

    input_path = Path(sys.argv[1]).resolve()
    output_path = input_path.with_name(f"{input_path.stem}_youtube.mp4")

    media_info = MediaInspector().analyze(str(input_path))
    profile = ExportProfile.youtube()
    exporter = YouTubeExporter()

    print(f"Input file: {input_path}")
    print(f"Output file: {output_path}")
    print(f"Duration: {media_info.duration_seconds}")
    print("Export profile: YouTube")
    print(f"Video codec: {profile.video_codec}")
    print(f"Audio codec: {profile.audio_codec}")

    result_path = exporter.execute(str(input_path), str(output_path))
    print(f"Export result: {result_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
