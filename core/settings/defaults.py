"""Default application settings."""

from core.settings.model import AppSettings


def default_settings() -> AppSettings:
    return AppSettings(
        default_output_folder="",
        last_selected_folder="",
        remember_last_selected_folder=True,
        open_output_folder_after_export=True,
        default_export_target="X",
        ffmpeg_path="ffmpeg",
        ffprobe_path="ffprobe",
        x_smart_bitrate=True,
        x_audio_bitrate="128k",
        x_preset="p5",
        x_pixel_format="yuv420p",
        youtube_quality="18",
        youtube_audio_bitrate="320k",
        youtube_pixel_format="yuv420p",
        youtube_faststart=True,
    )
