"""Default application settings."""

from core.settings.model import AppSettings


def default_settings() -> AppSettings:
    return AppSettings(
        default_output_folder="",
        open_output_folder_after_export=True,
        default_export_target="X",
        ffmpeg_path="ffmpeg",
        ffprobe_path="ffprobe",
    )
