# Release Plan

This document prepares the `v1.2.0-rc.1` release candidate for Exile Creator Kit.

## Release Title

```text
Exile Creator Kit v1.2.0-rc.1
```

## Version

Target release candidate:

```text
v1.2.0-rc.1
```

Canonical version file:

```text
VERSION
```

## Release Goal

`v1.2.0-rc.1` validates the next creator workflow before the final `v1.2.0` release.

The release candidate focuses on:

- Premium UI direction.
- Smart Environment foundation.
- Export Preset System.
- Preflight enforcement.
- Hardened media inspection.
- Release candidate validation.

## GitHub Release Description

```markdown
# Exile Creator Kit v1.2.0-rc.1

This is a release candidate for Exile Creator Kit v1.2.0.

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
- Release Candidate checklist

## Requirements

- Windows 10 or later
- FFmpeg and FFprobe included in release builds
- NVIDIA GPU recommended for NVENC
- Software H.264 fallback available

## Notes

- This is an RC build, not the final v1.2.0 release.
- Please validate exports with test videos before using it for production work.
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
ExileCreatorKit-v1.2.0-rc.1-win64.zip
SHA256SUMS.txt
LICENSE
CHANGELOG.md
```

Required files inside the ZIP:

```text
ExileCreatorKit-v1.2.0-rc.1-win64/
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

Recommended `v1.2.0-rc.1` distribution:

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

- [ ] Confirm `VERSION` is `v1.2.0-rc.1`.
- [ ] Confirm About dialog shows `v1.2.0-rc.1`.
- [ ] Confirm README mentions `v1.2.0-rc.1`.
- [ ] Confirm CHANGELOG includes `v1.2.0-rc.1`.
- [ ] Confirm Git tag name: `v1.2.0-rc.1`.

### Documentation

- [ ] README release link is current.
- [ ] README feature list includes Smart Environment.
- [ ] README feature list includes Premium UI.
- [ ] README feature list includes Preset System.
- [ ] README screenshot is current.
- [ ] RC checklist exists.

### Build Assets

- [ ] Confirm `vendor/ffmpeg/ffmpeg.exe` exists.
- [ ] Confirm `vendor/ffmpeg/ffprobe.exe` exists.
- [ ] Confirm application icon exists.
- [ ] Confirm release ZIP includes license files.
- [ ] Confirm third-party notices exist.

### Build

- [ ] Run PyInstaller using `packaging/pyinstaller.spec`.
- [ ] Confirm `dist/ExileCreatorKit/ExileCreatorKit.exe` exists.
- [ ] Confirm `ffmpeg.exe` is bundled.
- [ ] Confirm `ffprobe.exe` is bundled.
- [ ] Create portable ZIP.
- [ ] Generate SHA256 checksum.

### Runtime Validation

- [ ] Complete `docs/RC_CHECKLIST.md`.
- [ ] Launch from Explorer.
- [ ] Launch from Command Prompt.
- [ ] Launch from a path containing spaces.
- [ ] Select supported videos.
- [ ] Drop supported videos.
- [ ] Validate preset selection.
- [ ] Validate Preflight OK / Warning / Error.
- [ ] Export using X preset.
- [ ] Export using YouTube preset.
- [ ] Export using YouTube Shorts preset.
- [ ] Export using Discord preset.
- [ ] Export using Custom preset.
- [ ] Confirm output files are playable.
- [ ] Confirm settings persist in AppData.
- [ ] Confirm export history persists in AppData.

### GitHub Release

- [ ] Start from a clean working tree.
- [ ] Create release commit.
- [ ] Create `v1.2.0-rc.1` tag.
- [ ] Draft GitHub Release.
- [ ] Paste release description.
- [ ] Attach ZIP.
- [ ] Attach checksum file.
- [ ] Attach screenshots if ready.
- [ ] Mark as pre-release.
- [ ] Publish.
- [ ] Verify release page after publishing.

## Remaining Work

- Complete RC validation.
- Update screenshot assets if needed.
- Build the distributable ZIP.
- Generate checksums.
- Publish GitHub pre-release after validation passes.
