# Current Spec

Last updated: 2026-07-09

## Project Purpose

Exile Creator Kit is a desktop video export tool for Path of Exile and Path of Exile 2 creators.

The v1.0 goal is to help creators produce upload-ready videos for X and YouTube without needing to understand FFmpeg details.

## Current Scope

- Desktop GUI is the primary user entry point.
- Supported export targets are X and YouTube.
- FFmpeg is used for video export.
- FFprobe is used for media analysis.
- Preferred hardware encoder: NVIDIA NVENC when available.
- Smart Bitrate is used for the X 512 MB-oriented workflow.
- Settings are loaded and saved through the settings system.
- Export history and export queue models support the GUI workflow.

## Supported Input Files

- `.mp4`
- `.mkv`
- `.mov`
- `.avi`

## User Workflow

```text
Open Exile Creator Kit
        |
Choose or drop a video
        |
Review selected-video information
        |
Choose an export target
        |
Export video
        |
Review result and open output folder
```

## Media Inspector

Media Inspector is the shared module for analyzing video files.

### Role

- Analyze video files.
- Return media metadata as a MediaInfo instance.
- Do not convert, transcode, compress, or modify video files.

### Information To Retrieve

- File name
- Extension
- Video duration
- File size
- Video codec
- Audio codec
- Resolution
- FPS
- Video bitrate
- Audio bitrate
- Total bitrate

## Smart Bitrate

Smart Bitrate calculates a recommended video bitrate for X exports.

### Role

- Use video duration to calculate a target video bitrate.
- Keep the X export workflow oriented around a 512 MB output limit.
- Reserve room for audio bitrate and container overhead.
- Clamp extremely short and extremely long videos to reasonable limits.

## Export Targets

### X

The X export workflow is optimized for posting videos to X.

- H.264 output
- AAC audio
- Smart Bitrate for the 512 MB-oriented workflow
- Fast start metadata when supported
- User-facing label: `Export for X (512 MB)`

### YouTube

The YouTube export workflow is a higher-quality export for upload.

- H.264 output
- AAC audio
- Higher-quality export profile than X
- Fast start metadata when supported
- User-facing label: `Export for YouTube (High Quality)`

## GUI

The GUI should allow the user to:

- choose a video file
- drag and drop a supported video file
- view selected-video information
- start X export
- start YouTube export
- see progress and result status
- see friendly error messages
- open the output folder after export
- view recent exports
- open Settings
- open About

## Settings

Settings are managed through SettingsService.

Current General settings include:

- default output folder
- open output folder after export
- remember last selected folder
- last selected folder

## Release Scope

v1.0 includes:

- Desktop GUI
- Media Inspector
- Smart Bitrate for X
- X export
- YouTube export
- Settings
- Recent Exports
- Export queue foundation
- Export history foundation
- Release checklist

v1.0 excludes:

- OBS integration
- Publishing account integration
- Automatic upload to X
- Automatic upload to YouTube
- Timeline editing
- Clip cutting
- Subtitle editing
- Thumbnail generation
- Plugin system

## Video File Policy

Video files are not managed by Git.

Use an external storage location for source videos, generated videos, and other large media files.

The project default media storage location is:

```text
D:\ExileCreatorKit
```

## Protected Areas

Do not change files under:

```text
scripts/
```
