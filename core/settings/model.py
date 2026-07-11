"""Settings data models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AppSettings:
    default_output_folder: str
    last_selected_folder: str
    remember_last_selected_folder: bool
    open_output_folder_after_export: bool
    default_export_target: str
    default_export_preset: str
    encoder: str
    ffmpeg_path: str
    ffprobe_path: str
    x_smart_bitrate: bool
    x_audio_bitrate: str
    x_preset: str
    x_pixel_format: str
    youtube_quality: str
    youtube_audio_bitrate: str
    youtube_pixel_format: str
    youtube_faststart: bool
