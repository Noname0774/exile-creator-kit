# Changelog

All notable changes to Exile Creator Kit will be documented in this file.

## v1.2.0 - Official Release

### Added

- Premium dark UI foundation with componentized GUI cards.
- Smart Environment foundation:
  - GPU detection.
  - Environment information.
  - Encoder decision support.
  - Diagnostics foundation.
- Export Preset system:
  - X (512 MB).
  - YouTube (High Quality).
  - YouTube Shorts.
  - Discord.
  - Custom.
- Preset selector in the Export card.
- Default Export Preset setting.
- Preflight checks before export.
- Preflight Warning confirmation flow.
- Release validation checklist for v1.2.0.

### Changed

- Export workflow now applies the selected preset to FFmpeg settings.
- Settings window has been modernized for the v1.2 UI direction.
- Media summary display is connected to the Premium UI.
- Status card now displays environment readiness information.
- FFprobe parsing is hardened for invalid JSON, empty data, corrupted media, and unexpected values.

### Improved

- Export is blocked when Preflight returns Error.
- Export requires confirmation when Preflight returns Warning.
- Media inspection failures now return safer user-facing errors.
- Preset selections are saved and restored through SettingsService.

## v1.1.0 - Unreleased

### Added

- Encoder selection settings:
  - Auto (Recommended)
  - NVIDIA NVENC
  - Software (libx264)
- Automatic software encoder fallback when hardware encoding fails.
- Session-based software encoder preference after successful fallback.
- Successful export diagnostics logs.
- Export logs now record:
  - Selected encoder setting.
  - Actual video codec used.
  - FFmpeg command.
  - Output path.
  - Export target.

### Changed

- Export profiles now respect the selected encoder setting.
- Export workflow now provides better diagnostics for troubleshooting.

### Improved

- Users can verify which encoder was actually used after export.

## v1.0.0 - Pending

First public release.

### Added

- Desktop GUI as the primary user entry point.
- Video selection through file picker.
- Native drag-and-drop support.
- MediaInfo display for selected videos.
- X export workflow.
- YouTube export workflow.
- Smart Bitrate support for X exports.
- FFmpeg and FFprobe integration.
- Export profiles.
- Generic exporter framework.
- Export queue foundation.
- Export history foundation.
- Recent Exports panel.
- Settings foundation.
- Settings window.
- About dialog using the canonical `VERSION` file.
- Friendly export status and error messages.
- Application data storage under `%APPDATA%\Exile Creator Kit`.
- Packaging design documentation.
- PyInstaller packaging configuration.
- Build guide for the first distributable Windows build.
- Release asset checklist.
- GitHub release plan.

### Changed

- Settings and export history use stable AppData-based storage.
- Packaging direction is standardized around PyInstaller `onedir`.
- Project metadata now uses `VERSION` as the canonical version source.

### Known Limitations

- Real FFmpeg progress percentage is not shown yet.
- Export cancellation is not available yet.
- Advanced batch queue management is not available yet.
- Installer and auto-update are not included yet.
- Code signing may be deferred.

## Pre-v1.0 Development History

### Added

- Initial Core media inspection modules.
- `MediaInfo` data model.
- FFprobe adapter and parser.
- Smart Bitrate calculation.
- X and YouTube exporter foundations.
- Shared export profile model.
- Shared generic exporter.
- Validation tools.
- GUI prototype.
- Creator dashboard design.
- Runtime validation planning.
- Release checklist.
- v1.0 master plan.

### Changed

- GUI became the primary user workflow.
- Export workflow moved toward shared Core services.
- Settings access moved through `SettingsService`.
- Export history moved toward `ExportHistory` as the source of truth.
