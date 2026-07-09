# Architecture

## Current v1.0 Structure

```text
Exile Creator Kit
|
+-- README.md
+-- requirements.txt
+-- docs
|   |
|   +-- V1_MASTER_PLAN.md
|   +-- CURRENT_SPEC.md
|   +-- ARCHITECTURE.md
|   +-- DEVELOPMENT_GUIDE.md
|   +-- DASHBOARD.md
|   +-- RELEASE_CHECKLIST.md
|   +-- DEV_LOG.md
|
+-- core
|   |
|   +-- media
|   |   |
|   |   +-- MediaInspector
|   |   +-- MediaInfo
|   |   +-- FFprobeAdapter
|   |   +-- FFprobeParser
|   |   +-- SmartBitrate
|   |
|   +-- export
|   |   |
|   |   +-- ExportProfile
|   |   +-- GenericExporter
|   |   +-- XExporter
|   |   +-- YouTubeExporter
|   |   +-- ExportQueue
|   |   +-- ExportHistory
|   |
|   +-- settings
|       |
|       +-- AppSettings
|       +-- SettingsRepository
|       +-- SettingsService
|       +-- SettingsValidator
|
+-- gui
|   |
|   +-- Main Window
|   +-- Settings Window
|   +-- About Window
|
+-- tools
|   |
|   +-- Export.bat
|   +-- export.py
|   +-- ExportToX.bat
|   +-- export_to_x.py
|   +-- ExportToYouTube.bat
|   +-- export_to_youtube.py
|   +-- ValidateMedia.bat
|   +-- validate_media_inspector.py
|
+-- scripts
```

## Runtime Flow

```text
GUI
 |
 +-- choose or drop video
 |
 +-- MediaInspector
 |     |
 |     +-- FFprobeAdapter
 |     +-- FFprobeParser
 |     +-- MediaInfo
 |
 +-- export target
 |     |
 |     +-- ExportQueue
 |     +-- XExporter / YouTubeExporter
 |     +-- GenericExporter
 |     +-- ExportProfile
 |
 +-- ExportHistory
 |
 +-- SettingsService
```

## Roles

- `core/media`: video analysis and media metadata
- `core/export`: export profiles, command building, execution, queue, and history
- `core/settings`: application settings model, validation, persistence, and service entry point
- `gui`: user-facing desktop workflow
- `tools`: validation and batch entry points
- `docs`: project direction, specification, architecture, and release process
- `scripts`: protected area

## Architecture Principles

- Core owns reusable application logic.
- GUI coordinates user workflow but does not duplicate Core logic.
- Media modules analyze videos only.
- Export modules build and execute export workflows.
- Settings are accessed through SettingsService.
- ExportHistory is the source of truth for completed exports.
- ExportQueue is the entry point for queued GUI exports.
- FFmpeg and FFprobe details stay outside the user-facing workflow.
- Large video files stay outside Git.

## v1.0 Boundaries

Included in v1.0:

- Desktop GUI
- Media Inspector
- Smart Bitrate for X
- X export
- YouTube export
- Settings
- Recent Exports
- Export queue foundation
- Export history foundation

Deferred to v1.1+:

- Full batch queue management
- Persistent export history
- Advanced export presets
- Per-target settings
- Real FFmpeg progress parsing
- Export cancellation
- Packaging installer
- OBS workflow support
- Publishing workflow support
