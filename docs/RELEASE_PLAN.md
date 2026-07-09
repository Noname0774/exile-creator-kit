# Release Plan

This document prepares the first public GitHub release for Exile Creator Kit.

## Release Title

```text
Exile Creator Kit v1.0.0
```

## Version

Target public release:

```text
v1.0.0
```

Current development version:

```text
v0.4.1-alpha
```

Before publishing, update all visible and metadata versions to `v1.0.0`.

## GitHub Release Description

```markdown
# Exile Creator Kit v1.0.0

Exile Creator Kit is a Windows desktop tool for creating upload-ready gameplay videos for X and YouTube.

This first public release focuses on a simple creator workflow:

- choose or drop a video
- review basic media information
- export for X with a 512 MB-oriented workflow
- export for YouTube with a high-quality workflow
- open the output folder after export
- manage basic settings
- see recent export results

## Included

- Desktop GUI
- File picker and drag-and-drop video selection
- MediaInfo display
- X export
- YouTube export
- Smart Bitrate for X
- FFmpeg and FFprobe integration
- Export profiles
- Export queue foundation
- Export history foundation
- Settings window
- About dialog
- Friendly status and error messages

## Requirements

- Windows 10 or later
- NVIDIA NVENC-capable GPU recommended
- Bundled FFmpeg and FFprobe are included in the release ZIP

## Installation

1. Download `ExileCreatorKit-v1.0.0-win64.zip`.
2. Extract the ZIP.
3. Run `ExileCreatorKit.exe`.
4. Choose or drop a video file.
5. Export for X or YouTube.

## Notes

- Settings and export history are stored in `%APPDATA%\Exile Creator Kit`.
- Source videos and exported videos are never stored in Git or bundled with the app.
- This release does not upload videos automatically.
- This release does not include OBS integration.

## Known Issues

- Real FFmpeg progress percentage is not shown yet.
- Export cancellation is not available yet.
- Advanced batch queue management is not available yet.
- Installer and auto-update are not included yet.
- Code signing may not be available for the first public release.
```

## Assets

Required release assets:

```text
ExileCreatorKit-v1.0.0-win64.zip
SHA256SUMS.txt
LICENSE
CHANGELOG.md
```

Required files inside the ZIP:

```text
ExileCreatorKit-v1.0.0-win64/
|
+-- ExileCreatorKit.exe
+-- ffmpeg.exe
+-- ffprobe.exe
+-- _internal/
+-- tools/
+-- assets/
+-- LICENSES/
+-- README.txt
+-- CHANGELOG.txt
```

Required bundled notices:

```text
LICENSES/
|
+-- ExileCreatorKit.txt
+-- FFmpeg.txt
+-- THIRD_PARTY_NOTICES.txt
```

Optional assets:

```text
screenshots/
|
+-- main-window.png
+-- selected-video.png
+-- export-completed.png
+-- settings-window.png
```

## Installation

Recommended v1.0 distribution:

```text
Portable ZIP
```

User steps:

1. Download the release ZIP from GitHub Releases.
2. Extract it to any folder.
3. Run `ExileCreatorKit.exe`.

Do not require an installer for v1.0.

Do not store active settings beside the executable.

Application data location:

```text
%APPDATA%\Exile Creator Kit
```

## Known Issues

Known v1.0 limitations:

- No automatic upload to X.
- No automatic upload to YouTube.
- No OBS integration.
- No real FFmpeg progress parsing.
- No export cancellation.
- No advanced batch queue UI.
- No installer.
- No auto-update.
- Code signing may be deferred.

User-facing release notes should keep these limitations clear and short.

## Future Roadmap

Planned v1.1+ candidates:

- real FFmpeg progress display
- export cancellation
- advanced batch queue management
- persistent export history improvements
- per-target output folder rules
- packaged installer
- update checks
- crash reporting
- OBS workflow support
- publishing workflow support

Do not expand v1.0 scope during release preparation.

## Screenshots To Include

Recommended screenshots:

- main window with no video selected
- selected video information
- completed X export
- completed YouTube export
- settings window
- about dialog

Screenshot rules:

- use test videos only
- avoid personal file paths
- avoid copyrighted video frames unless permission is confirmed
- keep screenshots consistent with v1.0 UI

## Release Checklist

### Version

- [ ] Set canonical version to `v1.0.0`.
- [ ] Update About dialog version.
- [ ] Update CHANGELOG release date.
- [ ] Confirm Git tag name: `v1.0.0`.

### Legal

- [ ] Confirm final project copyright holder.
- [ ] Confirm MIT License text is final.
- [ ] Add FFmpeg license notice.
- [ ] Add third-party notices.
- [ ] Confirm FFmpeg redistribution terms.

### Build Assets

- [ ] Confirm `vendor/ffmpeg/ffmpeg.exe` exists.
- [ ] Confirm `vendor/ffmpeg/ffprobe.exe` exists.
- [ ] Confirm application icon exists or intentionally ship without one.
- [ ] Confirm release ZIP includes required license files.

### Build

- [ ] Install build dependencies.
- [ ] Run PyInstaller using `packaging/pyinstaller.spec`.
- [ ] Confirm `dist/ExileCreatorKit/ExileCreatorKit.exe` exists.
- [ ] Confirm `ffmpeg.exe` is beside `ExileCreatorKit.exe`.
- [ ] Confirm `ffprobe.exe` is beside `ExileCreatorKit.exe`.
- [ ] Create portable ZIP.
- [ ] Generate SHA256 checksum.

### Runtime Validation

- [ ] Launch app from Explorer.
- [ ] Launch app from Command Prompt.
- [ ] Launch app from a path containing spaces.
- [ ] Confirm Settings window opens.
- [ ] Confirm About dialog opens.
- [ ] Select a supported video.
- [ ] Drop a supported video.
- [ ] Confirm MediaInfo display.
- [ ] Export for X.
- [ ] Export for YouTube.
- [ ] Confirm output files are playable.
- [ ] Confirm Open Output Folder works.
- [ ] Confirm settings persist in AppData.
- [ ] Confirm export history persists in AppData.

### GitHub Release

- [ ] Start from a clean working tree.
- [ ] Create release commit.
- [ ] Create `v1.0.0` tag.
- [ ] Draft GitHub Release.
- [ ] Paste release description.
- [ ] Attach ZIP.
- [ ] Attach checksum file.
- [ ] Attach screenshots if ready.
- [ ] Mark as latest release.
- [ ] Publish.
- [ ] Verify release page after publishing.

## Remaining Work

- Finalize `v1.0.0` version updates.
- Confirm final copyright holder.
- Add FFmpeg and third-party license notices.
- Complete first PyInstaller build.
- Validate packaged runtime behavior.
- Capture screenshots.
- Assemble release ZIP.
- Generate checksums.
- Publish GitHub Release after validation passes.
