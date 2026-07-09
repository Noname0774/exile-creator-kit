# Changelog

All notable changes to Exile Creator Kit will be documented in this file.

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
