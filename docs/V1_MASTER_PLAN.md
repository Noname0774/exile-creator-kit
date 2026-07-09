# CK v1.0 Master Plan

This document defines the intended v1.0 scope for Exile Creator Kit.

After this document is accepted, v1.0 scope should not change casually.

## v1.0 Final Goal

Exile Creator Kit v1.0 is a creator-focused desktop tool for turning Path of Exile and Path of Exile 2 gameplay videos into upload-ready videos for X and YouTube.

The application should let a creator:

- choose or drop a video file
- review basic media information
- export for X with a 512 MB-oriented workflow
- export for YouTube with a high-quality workflow
- understand progress, success, and failure states
- adjust basic application settings
- complete the workflow without knowing FFmpeg details

## v1.0 Completion Criteria

v1.0 is complete when:

- the GUI is the primary user entry point
- video selection works through file picker and drag-and-drop
- Media Inspector displays reliable selected-video information
- X export works from the GUI
- YouTube export works from the GUI
- Smart Bitrate is applied to X exports
- completed exports show the output path
- users can open the output folder after export
- failed exports show friendly, actionable messages
- recent exports are visible in the GUI
- settings can be loaded, edited, saved, and reused
- release validation passes using the release checklist

## Features Included in v1.0

- Desktop GUI
- Video file selection
- Native drag-and-drop for supported video files
- Media Inspector integration
- MediaInfo display
- X export
- YouTube export
- Smart Bitrate for X
- FFmpeg execution
- FFprobe-based analysis
- Export profiles
- Generic exporter framework
- Export queue foundation
- Export history foundation
- Recent Exports panel
- General settings
- Settings window
- About dialog
- Output folder opening
- Friendly status and error messages
- Release checklist

## Features Excluded from v1.0

- OBS integration
- Publishing account integration
- Automatic upload to X
- Automatic upload to YouTube
- Stream overlay tools
- Advanced batch processing UI
- Cloud storage integration
- Project library or media database
- Timeline editing
- Clip cutting
- Subtitle editing
- Thumbnail generation
- Multi-language UI
- Plugin system

## Features Deferred to v1.1+

- Full batch queue management
- Persistent export history
- Advanced export presets
- Per-target settings for X and YouTube
- FFmpeg path configuration UI
- Export cancellation
- Real progress from FFmpeg output
- Output folder rules per target
- Packaging installer
- Crash reporting
- Update checks
- OBS workflow support
- Publishing workflow support

## Architecture Principles

- Core owns reusable application logic.
- GUI coordinates user workflow but does not duplicate Core logic.
- Media modules analyze videos only.
- Export modules build and execute export workflows.
- Settings are accessed through SettingsService.
- ExportHistory is the source of truth for completed exports.
- ExportQueue is the entry point for queued GUI exports.
- FFmpeg and FFprobe details should stay outside the user-facing workflow.
- Large video files must stay outside Git.

## Development Rules

- One Issue = One Commit.
- One Class = One Responsibility.
- Specification First.
- Small Commits.
- Core before Applications.
- Do not change architecture without review.
- README is user documentation.
- CURRENT_SPEC describes current behavior.
- ARCHITECTURE describes project structure.
- DEV_LOG records completed work only.
- Do not expand v1.0 scope without explicit review.

## Release Criteria

- README reflects the v1.0 user workflow.
- CURRENT_SPEC reflects actual v1.0 behavior.
- ARCHITECTURE reflects actual v1.0 structure.
- RELEASE_CHECKLIST is completed for the release.
- Application version is updated.
- Dependencies are documented.
- FFmpeg and FFprobe requirements are clear.
- Git working tree is clean before tagging.
- Git tag is created for v1.0.
- GitHub release is created from the v1.0 tag.

## Quality Criteria

- First launch is understandable without technical knowledge.
- Main workflow is clear from video selection to export completion.
- Export buttons use user-facing language.
- Selected-video information is readable.
- Failure messages avoid Python tracebacks.
- Exported files are playable.
- X exports target the 512 MB posting workflow.
- YouTube exports use a higher-quality workflow.
- Settings persist correctly across launches.
- The app can recover from missing FFmpeg or invalid input gracefully.

## Roadmap from v0.4-alpha to v1.0

### Phase 1: Scope Alignment

- Update project docs to match the actual GUI and export direction.
- Resolve outdated non-goals from earlier project phases.
- Confirm v1.0 included and excluded features.

### Phase 2: Workflow Stabilization

- Validate file picker and drag-and-drop behavior.
- Validate Media Inspector output in the GUI.
- Validate X export from the GUI.
- Validate YouTube export from the GUI.
- Confirm output path display and Open Output Folder behavior.

### Phase 3: Settings Stabilization

- Confirm SettingsService is the only settings entry point.
- Validate General settings save and load correctly.
- Confirm last selected folder behavior.
- Confirm output folder behavior.

### Phase 4: Export Reliability

- Confirm ExportQueue is used by GUI exports.
- Confirm ExportHistory records completed exports.
- Confirm Recent Exports reflects ExportHistory.
- Improve failure handling for FFmpeg, FFprobe, and invalid files.

### Phase 5: Release Hardening

- Complete runtime validation.
- Complete GUI validation.
- Complete export validation.
- Complete settings validation.
- Update user documentation.
- Prepare release notes.

### Phase 6: v1.0 Release

- Run the release checklist.
- Confirm release commit.
- Create v1.0 Git tag.
- Create GitHub release.
- Attach release artifacts if applicable.
