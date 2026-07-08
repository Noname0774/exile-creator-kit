"""Settings data models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AppSettings:
    default_output_folder: str
    open_output_folder_after_export: bool
    default_export_target: str
    ffmpeg_path: str
    ffprobe_path: str
