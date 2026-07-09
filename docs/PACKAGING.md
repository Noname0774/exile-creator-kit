# Packaging

This document defines the recommended Windows packaging direction for Exile Creator Kit v1.0.

## Summary

Recommended v1.0 approach:

- Use PyInstaller.
- Build a Windows folder distribution first.
- Include the GUI entry point.
- Bundle FFmpeg and FFprobe beside the application when licensing is confirmed.
- Store user data in `%APPDATA%\Exile Creator Kit`.
- Release a portable ZIP for v1.0.
- Defer installer, auto-update, and signing until after the first stable package.

## Build Tool Selection

### Recommended: PyInstaller

Use PyInstaller for v1.0 because:

- it supports tkinter applications well
- it is common for Python desktop tools
- it can produce a folder-based Windows distribution
- it allows bundling external binaries
- it keeps the packaging process simple for v1.0

Preferred build mode:

```text
onedir
```

Reason:

- easier to inspect
- easier to include FFmpeg and FFprobe
- easier to debug missing files
- safer than a single executable for the first release

### Alternative: Nuitka

Nuitka may be considered later if:

- startup time becomes a problem
- binary size becomes important
- stronger compiled output is needed

Do not use Nuitka for v1.0 unless PyInstaller cannot meet release needs.

## Architecture

```text
Source Tree
|
+-- gui
|   +-- main_window.py
|
+-- core
|   +-- media
|   +-- export
|   +-- settings
|   +-- storage
|
+-- tools
|   +-- export_to_x.py
|   +-- export_to_youtube.py
|
+-- vendor
    +-- ffmpeg
        +-- ffmpeg.exe
        +-- ffprobe.exe
```

```text
Build Output
|
+-- ExileCreatorKit
    |
    +-- ExileCreatorKit.exe
    +-- _internal
    |   +-- Python runtime files
    |   +-- application modules
    |
    +-- ffmpeg
        +-- ffmpeg.exe
        +-- ffprobe.exe
```

## Folder Structure After Build

Recommended v1.0 portable structure:

```text
ExileCreatorKit-v1.0.0-win64
|
+-- ExileCreatorKit.exe
+-- ffmpeg
|   |
|   +-- ffmpeg.exe
|   +-- ffprobe.exe
|
+-- _internal
|   |
|   +-- bundled application files
|
+-- README.txt
+-- LICENSES
    |
    +-- ExileCreatorKit.txt
    +-- FFmpeg.txt
```

The user should launch:

```text
ExileCreatorKit.exe
```

## Bundled Dependencies

Bundle:

- Python runtime
- tkinter runtime support
- application source modules
- required Python packages
- optional drag-and-drop dependency if still required
- FFmpeg executable
- FFprobe executable

Do not bundle:

- source videos
- exported videos
- user settings
- export history
- development cache files
- Git metadata

## FFmpeg and FFprobe Packaging Strategy

v1.0 should support two modes:

1. Bundled binaries
2. User-configured system binaries

Default packaged behavior:

- Prefer bundled `ffmpeg\ffmpeg.exe`.
- Prefer bundled `ffmpeg\ffprobe.exe`.
- Fall back to configured paths from settings.
- Fall back to system `ffmpeg` and `ffprobe` only when needed.

Packaging must include license notices for FFmpeg.

The exact FFmpeg build must be selected before release based on:

- license compatibility
- redistribution permission
- NVENC support
- Windows x64 support
- H.264 and AAC support

## AppData Usage

Packaged builds must use the same application data location as development builds:

```text
%APPDATA%\Exile Creator Kit
```

Stored files:

```text
%APPDATA%\Exile Creator Kit
|
+-- settings.json
+-- export_history.json
```

Application data must not be stored beside the executable.

This keeps behavior stable across:

- VS Code
- Command Prompt
- Explorer
- portable ZIP launch
- future installed application launch

## Installer Strategy

v1.0 recommendation:

- Do not require an installer.
- Ship a portable ZIP first.

Installer can be added after v1.0 when:

- the portable package is validated
- AppData behavior is stable
- FFmpeg bundling is legally confirmed
- signing strategy is decided

Future installer candidates:

- Inno Setup
- WiX Toolset
- MSIX

Recommended future first installer:

```text
Inno Setup
```

Reason:

- simple Windows installer flow
- good shortcut support
- easy uninstall entry
- practical for small desktop applications

## Portable Version Strategy

v1.0 should provide a portable ZIP:

```text
ExileCreatorKit-v1.0.0-win64.zip
```

Portable behavior:

- unzip anywhere
- run `ExileCreatorKit.exe`
- store settings in AppData
- store history in AppData
- export videos to the selected output folder or beside the source video

Portable builds should not write active configuration into the unzipped folder.

## Update Strategy

Auto-update is deferred to v1.1+.

v1.0 update process:

1. Download the new ZIP.
2. Close Exile Creator Kit.
3. Extract the new folder.
4. Run the new executable.
5. Reuse existing AppData settings and history.

Future update options:

- manual update notification
- GitHub release check
- installer-based upgrade
- signed auto-updater

Do not implement auto-update for v1.0.

## Signing Considerations

Code signing is deferred to a future release unless release distribution requires it.

Future signing goals:

- sign `ExileCreatorKit.exe`
- sign installer if one exists
- reduce Windows SmartScreen warnings
- preserve release integrity

v1.0 may ship unsigned if:

- release notes clearly state this
- checksums are provided
- GitHub release artifacts are attached from a clean build

## Recommended Implementation

### Phase 1: Package Design Lock

- Confirm PyInstaller `onedir`.
- Confirm GUI entry point.
- Confirm portable ZIP as v1.0 release artifact.
- Confirm AppData remains the only active data location.

### Phase 2: Build Configuration

- Create PyInstaller build configuration.
- Exclude development-only files.
- Include required runtime dependencies.
- Include drag-and-drop dependency if required.

### Phase 3: FFmpeg Packaging

- Select redistributable Windows FFmpeg build.
- Confirm NVENC support.
- Add FFmpeg and FFprobe to package layout.
- Add license notices.

### Phase 4: Runtime Path Resolution

- Ensure packaged app can locate bundled FFmpeg and FFprobe.
- Preserve SettingsService overrides.
- Preserve system-path fallback.

### Phase 5: Release Validation

Validate packaged build from:

- extracted ZIP folder
- Explorer double-click
- Command Prompt
- folder path containing spaces
- fresh user AppData
- existing migrated AppData

## v1.0 Recommendation

Ship v1.0 as:

```text
PyInstaller onedir portable ZIP
```

Do not make an installer the v1.0 blocker.

Do not implement auto-update for v1.0.

Do not require code signing for v1.0 unless release distribution demands it.

Focus v1.0 packaging on:

- reliable GUI startup
- bundled FFmpeg and FFprobe
- stable AppData storage
- clear release notes
- repeatable build steps

## Remaining Work

- Create PyInstaller build configuration.
- Decide final FFmpeg distribution source.
- Verify FFmpeg license requirements.
- Add bundled FFmpeg path resolution.
- Build the first portable package.
- Run runtime validation against packaged output.
- Add release artifact checksums.
- Decide whether signing is required before public distribution.
