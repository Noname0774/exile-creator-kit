# Creator Dashboard

## Purpose

The Creator Dashboard is the future main screen for Exile Creator Kit.

It should help a creator select a video, review the media details, choose an export target, and start an export without needing to understand FFmpeg.

## Main Screen

```text
Exile Creator Kit
--------------------------------------------------

[ Selected Video ]

[ Media Information ]

[ Export Targets ]

[ Export Status ]

--------------------------------------------------
```

## Sections

### Selected Video

Shows the current video selected by the user.

Information:

- File name
- File path
- File size

Primary action:

- Select video

### Media Information

Shows the analyzed metadata from Media Inspector.

Information:

- Duration
- Resolution
- FPS
- Video codec
- Audio codec
- Current bitrate
- Recommended X bitrate

### Export Targets

Shows available export actions.

Buttons:

- Export for X
- Export for YouTube

Button descriptions:

- Export for X: optimized for X posting and the 512 MB target.
- Export for YouTube: high quality export for upload.

### Export Status

Shows the current export state.

Information:

- Idle
- Analyzing
- Exporting
- Complete
- Failed

When complete, show:

- Output file path
- Export target

## User Flow

```text
Open Dashboard
      |
Select Video
      |
Media Inspector analyzes video
      |
Dashboard displays media information
      |
User chooses export target
      |
Exporter creates output video
      |
Dashboard shows result
```

## Notes

- The dashboard should use existing Core modules.
- The dashboard should not duplicate export logic.
- The dashboard should hide FFmpeg details from the user.
- The dashboard should keep X and YouTube choices simple and clear.

