# Release Plan

This document records the completed `v1.2.0` official release plan for Exile Creator Kit.

## Release Title

```text
Exile Creator Kit v1.2.0
```

## Version

Official release:

```text
v1.2.0
```

Canonical version file:

```text
VERSION
```

## Release Goal

`v1.2.0` completes the Premium UI and creator workflow release.

The official release includes:

- Premium UI direction.
- Smart Environment foundation.
- Export Preset System.
- Preflight enforcement.
- Hardened media inspection.
- Release validation.

## GitHub Release Description

```markdown
# Exile Creator Kit v1.2.0

This is the official v1.2.0 release of Exile Creator Kit.

It introduces the next creator workflow:

- Premium dark UI
- Smart Environment detection
- GPU and encoder readiness display
- Export Preset System
- Preflight checks before export
- safer media inspection and FFprobe error handling

## Included

- X (512 MB) preset
- YouTube (High Quality) preset
- YouTube Shorts preset
- Discord preset
- Custom preset
- Settings support for default export preset
- Settings support for encoder behavior
- Preflight OK / Warning / Error flow
- Release validation checklist

## Requirements

- Windows 10 or later
- FFmpeg and FFprobe included in release builds
- NVIDIA GPU recommended for NVENC
- Software H.264 fallback available

## Notes

- This is the official v1.2.0 release build.
- Please validate exports with your own workflow before production use.
- Settings and export history are stored in AppData.

## Known Issues

- Real FFmpeg progress percentage is not shown yet.
- Export cancellation is not available yet.
- Advanced batch queue management is not available yet.
- Installer and auto-update are not included yet.
- Code signing may be deferred.
```

## Assets

Required release assets:

```text
ExileCreatorKit-v1.2.0-windows-x64.zip
SHA256SUMS.txt
LICENSE
CHANGELOG.md
```

Required files inside the ZIP:

```text
ExileCreatorKit-v1.2.0-windows-x64/
|
+-- ExileCreatorKit.exe
+-- ffmpeg.exe
+-- ffprobe.exe
+-- _internal/
+-- assets/
+-- LICENSES/
+-- README.txt
+-- CHANGELOG.txt
```

Required bundled notices:

```text
LICENSES/
|
+-- FFmpeg.txt
+-- THIRD_PARTY_NOTICES.txt
```

Recommended screenshots:

```text
screenshots/
|
+-- main-window.png
+-- settings-window.png
+-- preset-selector.png
+-- preflight-warning.png
+-- export-completed.png
```

## Installation

Recommended `v1.2.0` distribution:

```text
Portable ZIP
```

User steps:

1. Download the release ZIP from GitHub Releases.
2. Extract it to any folder.
3. Run `ExileCreatorKit.exe`.
4. Choose or drop a video file.
5. Select an export preset.
6. Export for X or YouTube.

Application data location:

```text
%APPDATA%\Exile Creator Kit
```

## Validation

Use:

```text
docs/RC_CHECKLIST.md
```

Required validation areas:

- Startup
- GPU Detection
- Encoder Auto
- Environment
- Diagnostics
- Media Summary
- Preflight
- Export
- Presets
- Settings
- UI
- Packaging
- README
- Release Assets

## Release Checklist

### Version

- [x] Confirm `VERSION` is `v1.2.0`.
- [x] Confirm About dialog shows `v1.2.0`.
- [x] Confirm README mentions `v1.2.0`.
- [x] Confirm CHANGELOG includes `v1.2.0`.
- [x] Confirm Git tag name: `v1.2.0`.

### Documentation

- [x] README release link is current.
- [x] README feature list includes Smart Environment.
- [x] README feature list includes Premium UI.
- [x] README feature list includes Preset System.
- [x] README screenshot is current.
- [x] Release checklist exists.

### Build Assets

- [x] Confirm `vendor/ffmpeg/ffmpeg.exe` exists.
- [x] Confirm `vendor/ffmpeg/ffprobe.exe` exists.
- [x] Confirm application icon exists.
- [x] Confirm release ZIP includes license files.
- [x] Confirm third-party notices exist.

### Build

- [x] Run PyInstaller using `packaging/pyinstaller.spec`.
- [x] Confirm `dist/ExileCreatorKit/ExileCreatorKit.exe` exists.
- [x] Confirm `ffmpeg.exe` is bundled.
- [x] Confirm `ffprobe.exe` is bundled.
- [x] Create portable ZIP.
- [x] Generate SHA256 checksum.

### Runtime Validation

- [x] Complete release validation checklist.
- [x] Launch from Explorer.
- [x] Launch from Command Prompt.
- [x] Launch from a path containing spaces.
- [x] Select supported videos.
- [x] Drop supported videos.
- [x] Validate preset selection.
- [x] Validate Preflight OK / Warning / Error.
- [x] Export using X preset.
- [x] Export using YouTube preset.
- [x] Export using YouTube Shorts preset.
- [x] Export using Discord preset.
- [x] Export using Custom preset.
- [x] Confirm output files are playable.
- [x] Confirm settings persist in AppData.
- [x] Confirm export history persists in AppData.

### GitHub Release

- [x] Start from a clean working tree.
- [ ] Create release commit.
- [ ] Create `v1.2.0` tag.
- [ ] Draft GitHub Release.
- [ ] Paste release description.
- [ ] Attach ZIP.
- [ ] Attach checksum file.
- [ ] Attach screenshots if ready.
- [ ] Publish as official release.
- [ ] Verify release page after publishing.

## Status

Completed for v1.2.0 release preparation.

Manual publishing steps remain:

- Create the release commit.
- Create the `v1.2.0` tag.
- Publish the GitHub Release.
