# Architecture

## Current

```text
Exile Creator Kit
|
+-- README
+-- docs
|   |
|   +-- CURRENT_SPEC
|   +-- DEV_LOG
|   +-- ARCHITECTURE
|
+-- Core
    |
    +-- Media Inspector
    |   |
    |   +-- MediaInfo
    |
    +-- Smart Bitrate
    |
    +-- Encoder
```

## Roles

- Core: shared project logic
- Media Inspector: video file analysis
- MediaInfo: analyzed media metadata
- Smart Bitrate: bitrate planning for 512 MB output
- Encoder: video output processing

## Future

```text
Future
|
+-- Publishing
+-- OBS
+-- GUI
```

