# Export Presets

This document defines the v1.0 export preset architecture before implementation.

The goal is to make SettingsService, ExportProfile, and Exporters work together without mixing responsibilities.

## 1. Architecture

```text
GUI
 |
 +-- SettingsService
 |     |
 |     +-- AppSettings
 |
 +-- Export Target
       |
       +-- XExporter / YouTubeExporter
             |
             +-- ExportProfile
             |
             +-- GenericExporter
                   |
                   +-- FFmpeg command
```

### Rule

SettingsService provides application and user preference values.

ExportProfile defines export preset values.

Exporters select and apply the correct profile.

GenericExporter builds and executes the FFmpeg command.

## 2. Data Flow

```text
User selects export target
        |
GUI loads settings through SettingsService
        |
GUI calls XExporter or YouTubeExporter
        |
Exporter selects ExportProfile.x() or ExportProfile.youtube()
        |
Exporter passes profile to GenericExporter
        |
GenericExporter builds FFmpeg command
        |
GenericExporter executes FFmpeg
        |
GUI records result and refreshes history
```

For X exports:

```text
MediaInfo.duration_seconds
        |
SmartBitrate.calculate()
        |
video_bitrate
        |
XExporter
        |
GenericExporter
```

## 3. Responsibility of Each Component

### SettingsService

SettingsService is the only public API for application settings.

Responsibilities:

- load settings
- save settings
- provide current AppSettings
- update AppSettings
- expose user preferences to GUI and future workflow code

SettingsService should not:

- build FFmpeg commands
- execute FFmpeg
- calculate bitrate
- own export profile defaults
- know target-specific encoding details

### AppSettings

AppSettings stores user preferences and application-level configuration.

v1.0 settings may affect:

- default output folder
- last selected folder
- whether to remember the last selected folder
- whether to open the output folder after export
- default export target
- FFmpeg path
- FFprobe path

AppSettings should not replace ExportProfile.

### ExportProfile

ExportProfile is an immutable model for target-specific export defaults.

Responsibilities:

- define video codec
- define audio codec
- define encoder preset
- define quality setting
- define audio bitrate
- define faststart behavior
- define pixel format
- provide factory methods for known targets

ExportProfile should not:

- read settings files
- execute FFmpeg
- inspect media files
- decide output paths
- store runtime export status

### XExporter

XExporter owns the X export workflow.

Responsibilities:

- use ExportProfile.x()
- accept optional video bitrate
- pass the profile and bitrate to GenericExporter
- preserve the public X export API

XExporter should not:

- duplicate GenericExporter command-building logic
- read or save settings directly
- calculate Smart Bitrate internally unless explicitly designed later

### YouTubeExporter

YouTubeExporter owns the YouTube export workflow.

Responsibilities:

- use ExportProfile.youtube()
- pass the profile to GenericExporter
- preserve the public YouTube export API

YouTubeExporter should not:

- duplicate GenericExporter command-building logic
- read or save settings directly
- use X-specific Smart Bitrate rules

### GenericExporter

GenericExporter is the shared FFmpeg command builder and executor.

Responsibilities:

- receive an ExportProfile
- build a Windows-safe FFmpeg command
- apply optional video bitrate when provided
- execute FFmpeg
- raise RuntimeError on failure
- return output path on success

GenericExporter should not:

- choose export targets
- load settings
- inspect media files
- update GUI state
- update export history

## 4. X Preset Flow

```text
GUI starts X export
        |
MediaInspector provides MediaInfo
        |
SmartBitrate calculates video bitrate
        |
XExporter.export(input, output, video_bitrate)
        |
XExporter uses ExportProfile.x()
        |
GenericExporter builds command
        |
XExporter.execute(input, output, video_bitrate)
        |
GenericExporter executes FFmpeg
```

X export is optimized for posting to X.

The X preset must prioritize:

- 512 MB-oriented output size
- H.264 compatibility
- AAC audio
- faststart metadata
- yuv420p pixel format
- predictable output

## 5. YouTube Preset Flow

```text
GUI starts YouTube export
        |
MediaInspector provides MediaInfo
        |
YouTubeExporter.export(input, output)
        |
YouTubeExporter uses ExportProfile.youtube()
        |
GenericExporter builds command
        |
YouTubeExporter.execute(input, output)
        |
GenericExporter executes FFmpeg
```

YouTube export is optimized for higher quality upload.

The YouTube preset must prioritize:

- higher quality than X
- H.264 compatibility
- AAC audio
- faststart metadata
- yuv420p pixel format
- support for 1080p, 1440p, and ultrawide uploads

Smart Bitrate is not part of the v1.0 YouTube preset flow.

## 6. Default Values

### Shared Defaults

- video codec: H.264 NVENC
- audio codec: AAC
- pixel format: yuv420p
- faststart: enabled

### X Defaults

- target: X
- video codec: H.264 NVENC
- audio codec: AAC
- preset: X export preset
- quality: X-compatible quality setting
- audio bitrate: reserved for the 512 MB-oriented workflow
- video bitrate: provided by SmartBitrate
- faststart: enabled
- pixel format: yuv420p

### YouTube Defaults

- target: YouTube
- video codec: H.264 NVENC
- audio codec: AAC
- preset: higher-quality export preset
- quality: higher than X
- audio bitrate: higher-quality upload default
- video bitrate: profile-driven or command default
- faststart: enabled
- pixel format: yuv420p

## 7. Future Extensibility

v1.0 should keep presets simple and code-defined.

v1.1+ may add:

- editable per-target settings
- custom export profiles
- profile names
- profile descriptions
- preset validation rules
- FFmpeg path selection
- FFprobe path selection
- per-target output folder rules
- persistent export profile JSON
- real FFmpeg progress parsing
- export cancellation

Future preset settings should extend the existing model instead of moving export logic into the GUI.

## Final Architecture Decision

For v1.0:

- SettingsService owns user preferences.
- ExportProfile owns target preset defaults.
- XExporter and YouTubeExporter choose the correct profile.
- GenericExporter builds and executes the FFmpeg command.
- SmartBitrate is applied only to the X flow.
- GUI coordinates the workflow but does not own export rules.
