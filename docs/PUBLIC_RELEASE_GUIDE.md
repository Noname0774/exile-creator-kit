# Public Release Guide

This guide prepares the repository presentation for the first public GitHub release.

## Summary

Current public presentation status:

- README: usable, but needs public-release polish
- Repository topics: not documented yet
- Social preview: not prepared
- Application icon: not prepared
- Screenshots: not prepared
- Release screenshots: not captured
- Public release state: not ready for publishing

Recommended decision:

```text
No-Go until presentation assets and runtime validation are complete.
```

## Repository Presentation Checklist

Before publishing v1.0:

- [ ] README explains the app in one clear sentence.
- [ ] README includes quick installation steps for the portable ZIP.
- [ ] README includes supported video formats.
- [ ] README includes X and YouTube export descriptions.
- [ ] README includes screenshots.
- [ ] README links to release ZIP from GitHub Releases.
- [ ] README explains AppData storage briefly.
- [ ] README explains that source videos are not stored in Git.
- [ ] README includes license section.
- [ ] Repository topics are set.
- [ ] Social preview image is set.
- [ ] Application icon is prepared.
- [ ] Release screenshots are captured.
- [ ] GitHub Release description is ready.

## README Improvements

Recommended README structure for public release:

```text
# Exile Creator Kit

One-line product description

Screenshot

## What It Does

## Download

## Quick Start

## Features

## Supported Video Files

## Requirements

## Where Settings Are Stored

## Known Limitations

## Documentation

## License
```

Recommended opening description:

```text
Exile Creator Kit is a Windows desktop tool that turns Path of Exile gameplay videos into upload-ready files for X and YouTube.
```

Recommended quick start:

```text
1. Download the latest release ZIP.
2. Extract it.
3. Run ExileCreatorKit.exe.
4. Choose or drop a video.
5. Export for X or YouTube.
```

Recommended user-facing feature labels:

- Export for X (512 MB)
- Export for YouTube (High Quality)
- Media information before export
- Recent exports
- Settings window
- Open output folder after export

Avoid in the top README section:

- internal architecture details
- issue history
- implementation notes
- long FFmpeg explanations

## GitHub Page Improvements

Recommended repository description:

```text
Windows desktop tool for creating upload-ready Path of Exile videos for X and YouTube.
```

Recommended repository topics:

```text
path-of-exile
path-of-exile-2
video-export
ffmpeg
ffprobe
nvenc
youtube
twitter
x
desktop-app
tkinter
python
windows
creator-tools
video-compression
```

Recommended GitHub sidebar links:

- Website: leave blank unless a project page exists
- Releases: use GitHub Releases
- Packages: not needed for v1.0

Recommended pinned files:

- `README.md`
- `CHANGELOG.md`
- `docs/RELEASE_PLAN.md`

## Screenshot Plan

Capture screenshots from a clean packaged build.

Required screenshots:

```text
docs/images/main-window.png
docs/images/selected-video.png
docs/images/export-completed.png
docs/images/settings-window.png
```

Optional screenshots:

```text
docs/images/about-dialog.png
docs/images/export-failed.png
docs/images/recent-exports.png
```

Screenshot rules:

- use a test video file
- avoid personal folder names
- avoid private account names
- avoid copyrighted video frames unless permission is confirmed
- keep window size consistent
- use the v1.0 packaged build, not a development shell

Recommended screenshot order in README:

1. Main window
2. Selected video
3. Completed export
4. Settings window

## Icon Plan

Recommended icon path:

```text
assets/icons/exile-creator-kit.ico
```

Icon requirements:

- original artwork
- readable at 16x16, 32x32, 48x48, and 256x256
- Windows `.ico` format
- no official Path of Exile logos or art unless permission is confirmed
- no unlicensed game assets
- simple silhouette or creator-tool concept

Recommended visual direction:

- dark neutral background
- bright export/play symbol
- subtle video frame shape
- no detailed game imagery

Release usage:

- PyInstaller app icon
- GitHub social preview source
- README branding image if needed

## Social Preview Plan

Recommended size:

```text
1280 x 640
```

Recommended path:

```text
docs/images/social-preview.png
```

Recommended content:

- Exile Creator Kit
- Create upload-ready videos for X and YouTube
- simple app screenshot or clean visual background
- no crowded UI text
- no copyrighted game art

GitHub setup:

1. Open repository Settings.
2. Go to Social preview.
3. Upload `social-preview.png`.
4. Verify preview rendering.

## Public Release Readiness

Current readiness:

```text
Not ready
```

Ready when:

- README has public quick start.
- Screenshots are captured and linked.
- Application icon exists.
- Social preview exists.
- Release ZIP exists.
- Runtime validation passes.
- GitHub Release notes are final.
- Legal notices are complete.

## Remaining Work

- Polish README for public users.
- Add screenshots under `docs/images/`.
- Create application icon.
- Create GitHub social preview.
- Set repository description.
- Set repository topics.
- Finish legal notices.
- Complete packaged runtime validation.
- Create final release ZIP and checksum.
