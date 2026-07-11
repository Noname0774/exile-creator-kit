"""Export preset definitions for future preset selection."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ExportPreset:
    """Immutable export preset metadata."""

    name: str
    target_platform: str
    container: str
    video_codec: str
    audio_codec: str
    video_bitrate: str
    audio_bitrate: str
    resolution_rule: str
    fps_rule: str
    description: str


class PresetRepository:
    """In-memory repository for built-in export presets."""

    def __init__(self) -> None:
        self._presets = (
            ExportPreset(
                name="X (512 MB)",
                target_platform="X",
                container="mp4",
                video_codec="h264",
                audio_codec="aac",
                video_bitrate="smart",
                audio_bitrate="128k",
                resolution_rule="keep source resolution",
                fps_rule="keep source FPS",
                description="Upload-ready X export targeting the 512 MB limit.",
            ),
            ExportPreset(
                name="YouTube (High Quality)",
                target_platform="YouTube",
                container="mp4",
                video_codec="h264",
                audio_codec="aac",
                video_bitrate="quality based",
                audio_bitrate="320k",
                resolution_rule="keep source resolution",
                fps_rule="keep source FPS",
                description="High quality YouTube export for standard uploads.",
            ),
            ExportPreset(
                name="YouTube Shorts",
                target_platform="YouTube Shorts",
                container="mp4",
                video_codec="h264",
                audio_codec="aac",
                video_bitrate="quality based",
                audio_bitrate="192k",
                resolution_rule="vertical short-form preferred",
                fps_rule="keep source FPS",
                description="Short-form YouTube export preset foundation.",
            ),
            ExportPreset(
                name="Discord",
                target_platform="Discord",
                container="mp4",
                video_codec="h264",
                audio_codec="aac",
                video_bitrate="size aware",
                audio_bitrate="128k",
                resolution_rule="scale down when needed",
                fps_rule="keep source FPS",
                description="Discord-friendly export preset foundation.",
            ),
            ExportPreset(
                name="Custom",
                target_platform="Custom",
                container="mp4",
                video_codec="user selected",
                audio_codec="user selected",
                video_bitrate="user selected",
                audio_bitrate="user selected",
                resolution_rule="user selected",
                fps_rule="user selected",
                description="User-defined export preset foundation.",
            ),
        )

    def list_presets(self) -> tuple[ExportPreset, ...]:
        """Return all available presets."""
        return self._presets

    def list_names(self) -> tuple[str, ...]:
        """Return preset display names."""
        return tuple(preset.name for preset in self._presets)

    def get_by_name(self, name: str) -> ExportPreset | None:
        """Return a preset by display name."""
        for preset in self._presets:
            if preset.name == name:
                return preset

        return None
