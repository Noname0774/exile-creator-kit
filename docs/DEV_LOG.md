# Development Log

## 2026-07-08

### Foundation Documentation

- Created the initial project README.
- Added the current project specification.
- Added this development log.
- Added Git ignore rules for local media, generated output, logs, and common tool artifacts.

### Decisions

- The project targets both Path of Exile and Path of Exile 2 video workflows.
- FFmpeg is the video processing backend.
- RTX 4090 NVENC is the intended encoding path.
- The first feature is X (Twitter) video compression.
- Video files are stored outside the repository at `D:\ExileCreatorKit`.

### Out of Scope For This Step

- GUI
- YouTube support
- Right-click registration
- Automatic bitrate calculation
- Batch file changes
- Any additional feature implementation

