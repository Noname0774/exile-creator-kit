"""Export a media file for X using the current core pipeline."""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from core.export import XExporter  # noqa: E402
from core.media.inspector import MediaInspector  # noqa: E402
from core.media.smart_bitrate import SmartBitrate  # noqa: E402


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python tools/export_to_x.py <media-file>")
        return 1

    input_path = Path(sys.argv[1]).resolve()
    output_path = input_path.with_name(f"{input_path.stem}_x.mp4")

    media_info = MediaInspector().analyze(str(input_path))
    recommended_bitrate = SmartBitrate().calculate(media_info.duration_seconds)
    exporter = XExporter()

    print(f"Input file: {input_path}")
    print(f"Output file: {output_path}")
    print(f"Duration: {media_info.duration_seconds}")
    print(f"Using bitrate: {recommended_bitrate}")

    result_path = exporter.execute(
        str(input_path),
        str(output_path),
        recommended_bitrate,
    )
    print(f"Export result: {result_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
