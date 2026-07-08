# Current Spec

Last updated: 2026-07-08

## Project Purpose

Exile Creator Kit is a shared video creation tool project for Path of Exile and Path of Exile 2.

## Current Scope

- Use FFmpeg for video processing.
- Use NVIDIA NVENC hardware encoding.
- Preferred hardware encoder: NVIDIA NVENC when available.
- Keep the workflow simple and foundation-focused before adding user-facing integrations.

## First Feature

The first feature is video compression for X (Twitter).

The project should prioritize producing videos suitable for posting to X while keeping the implementation limited to the agreed scope.

## Smart Bitrate Calculation

Smart Bitrate Calculation is a planned specification for automatically calculating the optimal video bitrate from the video's duration.

The purpose is to produce an output video that stays at or below 512 MB while preserving as much quality as possible within that file size limit.

### Requirements

- Calculate the target bitrate from the source video duration.
- Use 512 MB as the maximum output file size.
- Choose the highest practical bitrate that keeps the estimated output size at or below 512 MB.
- Reserve enough room for audio bitrate and container overhead when calculating the video bitrate.
- Keep the calculation deterministic so the same duration and settings produce the same target bitrate.

### Current Status

This is a specification only.

No Smart Bitrate Calculation implementation exists yet, and this update does not add code or change scripts.

## Media Inspector

Media Inspector is a shared module for analyzing video files.

### Purpose

Analyze video files and expose media metadata for other modules.

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
- Estimated bitrate for the 512 MB limit

### MediaInfo

MediaInfo is designed as a dataclass that holds analyzed media metadata.

Fields:

- file_name
- extension
- duration_seconds
- file_size_bytes
- video_codec
- audio_codec
- width
- height
- fps
- video_bitrate
- audio_bitrate
- total_bitrate
- estimated_512mb_limit_bitrate

MediaInspector analyzes a video file and returns a MediaInfo instance.

### Role

This module only analyzes video files.

It does not convert, transcode, compress, or otherwise modify video files.

## Video File Policy

Video files are not managed by Git.

Use this external storage location for source videos, generated videos, and other large media files:

```text
D:\ExileCreatorKit
```

## Current Non-Goals

The following work must not be added in the current phase:

- GUI
- YouTube support
- Right-click registration
- Smart Bitrate Calculation implementation
- Batch file changes
- New features beyond the initial X video compression direction

## Protected Areas

Do not change files under:

```text
scripts/
```
