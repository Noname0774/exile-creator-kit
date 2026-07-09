"""Export a media file for X using the current core pipeline."""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from core.export import XExporter  # noqa: E402
from core.media.inspector import MediaInspector  # noqa: E402
from core.media.smart_bitrate import SmartBitrate  # noqa: E402
from core.settings import SettingsService  # noqa: E402


def resolve_output_path(
    input_path: str | Path,
    suffix: str,
    output_path: str | Path | None = None,
) -> Path:
    if output_path is not None:
        return Path(output_path).resolve()

    path = Path(input_path).resolve()
    settings = SettingsService().get_settings()
    output_folder = settings.default_output_folder
    if output_folder:
        output_directory = Path(output_folder)
        if output_directory.exists():
            return output_directory / f"{path.stem}{suffix}.mp4"

    return path.with_name(f"{path.stem}{suffix}.mp4")


def x_output_path(
    input_path: str | Path,
    output_path: str | Path | None = None,
) -> Path:
    return resolve_output_path(input_path, "_x", output_path)


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("Usage: python tools/export_to_x.py <media-file> [output-file]")
        return 1

    input_path = Path(sys.argv[1]).resolve()
    output_path = x_output_path(input_path, sys.argv[2] if len(sys.argv) == 3 else None)

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
