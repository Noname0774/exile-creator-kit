# Changelog

All notable changes to Exile Creator Kit will be documented in this file.

## v1.0.0 - Pending

Planned first public release.

### Added

- Placeholder for final v1.0 release notes.

### Known Limitations

- Release assets are still being prepared.
- Packaging validation is not complete.

## v0.4.1-alpha

Current alpha version.

### Added

- Application data storage design and implementation.
- Packaging design documentation.
- PyInstaller packaging configuration.
- Build guide for the first distributable Windows build.
- Release asset checklist.

### Changed

- Settings and export history storage moved toward stable AppData-based behavior.
- Packaging direction standardized around PyInstaller `onedir`.

### Known Limitations

- Public release assets are incomplete.
- FFmpeg and FFprobe binaries are not bundled yet.
- License decision is pending.
- Release ZIP has not been assembled.

## v0.4-alpha

Development milestone for the creator workflow.

### Added

- Desktop GUI prototype.
- Video selection through file picker.
- Native drag-and-drop support.
- MediaInfo display for selected videos.
- X export workflow.
- YouTube export workflow.
- Smart Bitrate support for X exports.
- Export profiles.
- Generic exporter framework.
- Export queue model.
- Export history model.
- Recent Exports panel.
- Settings foundation.
- Settings window.
- About dialog.
- Friendly export status and error messages.
- Runtime validation planning.
- Release checklist.
- v1.0 master plan.

### Changed

- GUI became the primary user entry point.
- Export workflow moved toward shared Core services.
- Settings access moved through `SettingsService`.
- Export history moved toward `ExportHistory` as the source of truth.

### Known Limitations

- Packaging was not complete.
- Release assets were not ready.
- FFmpeg and FFprobe handling still required release validation.
- Real FFmpeg progress parsing was deferred.
- Full batch queue management was deferred.
