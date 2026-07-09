# Exile Creator Kit

Exile Creator Kit is a desktop video export tool for Path of Exile and Path of Exile 2 creators.

It helps creators turn gameplay videos into upload-ready files for X and YouTube without needing to understand FFmpeg commands, codecs, or bitrate details.

## Version

Current release version: `v1.0.0`

## v1.0 Goal

Create upload-ready videos for X and YouTube.

The v1.0 workflow is:

```text
Choose or drop a video
        |
Review media information
        |
Choose X or YouTube export
        |
Export video
        |
Open the output folder
```

## v1.0 Features

- Desktop GUI
- Video file selection
- Native drag-and-drop for supported video files
- Media information display
- X export with a 512 MB-oriented workflow
- YouTube high-quality export
- Smart Bitrate for X exports
- FFmpeg-based video export
- FFprobe-based media analysis
- Export progress and result status
- Friendly error messages
- Recent Exports panel
- General settings
- Settings window
- About dialog

## Supported Video Files

- `.mp4`
- `.mkv`
- `.mov`
- `.avi`

## Requirements

- Python
- FFmpeg
- FFprobe
- NVIDIA NVENC is preferred when available

## Video File Policy

Video files are not managed by Git.

Use an external storage location for source videos, generated videos, and other large media files.

The project default media storage location is:

```text
D:\ExileCreatorKit
```

## Documentation

- `docs/V1_MASTER_PLAN.md`: v1.0 scope and roadmap
- `docs/CURRENT_SPEC.md`: current project behavior
- `docs/ARCHITECTURE.md`: project structure
- `docs/DEVELOPMENT_GUIDE.md`: development rules
- `docs/RELEASE_CHECKLIST.md`: release validation checklist
- `docs/DEV_LOG.md`: completed work log

## License

Exile Creator Kit is licensed under the MIT License.
