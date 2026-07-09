# Release Assets

This document lists every asset required before the first public release of Exile Creator Kit.

## Summary

Current release asset status:

- Application icon: missing
- FFmpeg binary: missing
- FFprobe binary: missing
- LICENSE files: missing
- Third-party notices: missing
- Screenshots: missing
- README images: missing
- GitHub release description: missing
- Version file: missing
- CHANGELOG: missing
- Release ZIP contents: not assembled

The first public release should not be published until all required assets are present and license obligations are reviewed.

## Release Asset Checklist

| Asset | Required | Optional | Missing | Recommended source | License considerations |
|---|---:|---:|---:|---|---|
| Application icon | Yes | No | Yes | Create original `.ico` under `assets/icons/` | Must be original or explicitly licensed for redistribution |
| FFmpeg binary | Yes | No | Yes | Redistributable Windows x64 FFmpeg build with NVENC support | Must include matching FFmpeg license notice and comply with build license |
| FFprobe binary | Yes | No | Yes | Same FFmpeg distribution as `ffmpeg.exe` | Must include same FFmpeg license notice |
| Application LICENSE file | Yes | No | Yes | Project root `LICENSE` or `LICENSES/ExileCreatorKit.txt` | Must define how Exile Creator Kit itself is distributed |
| FFmpeg license file | Yes | No | Yes | License text from selected FFmpeg build/distribution | Must match the exact bundled FFmpeg build |
| Third-party notices | Yes | No | Yes | `LICENSES/THIRD_PARTY_NOTICES.txt` | Include Python packages and bundled binary notices |
| Screenshots | No | Yes | Yes | Capture from release candidate GUI | Avoid showing personal file paths or private video content |
| README images | No | Yes | Yes | Use sanitized screenshots under `docs/images/` or `assets/readme/` | Images must be original and safe to redistribute |
| GitHub release description | Yes | No | Yes | Draft from release checklist and v1.0 scope | Must clearly state requirements, limitations, and unsigned status if applicable |
| Version file | Yes | No | Yes | Add a simple project version source before release | Must match About dialog, release ZIP, Git tag, and GitHub release |
| CHANGELOG | Yes | No | Yes | `CHANGELOG.md` | Must describe user-facing changes and known limitations |
| Release ZIP contents | Yes | No | Yes | Build output from PyInstaller `onedir` | Must exclude source videos, generated videos, caches, Git metadata, and local settings |

## Asset Details

### Application Icon

Status:

- Required: yes
- Missing: yes

Recommended location:

```text
assets/icons/exile-creator-kit.ico
```

Recommended source:

- original icon designed for Exile Creator Kit
- generated or commissioned asset with redistribution rights

License considerations:

- do not use Path of Exile official art unless permission is confirmed
- do not use unlicensed game assets
- keep the icon generic enough for an open-source creator tool

### FFmpeg Binary

Status:

- Required: yes
- Missing: yes

Recommended location:

```text
vendor/ffmpeg/ffmpeg.exe
```

Recommended source:

- reputable Windows x64 FFmpeg distribution
- must support H.264, AAC, and NVIDIA NVENC

License considerations:

- record the exact FFmpeg source and version
- include the matching FFmpeg license notice
- confirm whether the selected build is LGPL or GPL
- do not bundle a binary unless redistribution terms are understood

### FFprobe Binary

Status:

- Required: yes
- Missing: yes

Recommended location:

```text
vendor/ffmpeg/ffprobe.exe
```

Recommended source:

- same distribution package as `ffmpeg.exe`

License considerations:

- keep FFmpeg and FFprobe from the same release package
- include the same license and notices

### LICENSE Files

Status:

- Required: yes
- Missing: yes

Recommended locations:

```text
LICENSE
LICENSES/ExileCreatorKit.txt
LICENSES/FFmpeg.txt
```

Recommended source:

- project license chosen by the maintainer
- FFmpeg license from the selected binary distribution

License considerations:

- project license should be decided before public release
- FFmpeg license must match the bundled build
- third-party licenses must be included in the release ZIP

### Third-Party Notices

Status:

- Required: yes
- Missing: yes

Recommended location:

```text
LICENSES/THIRD_PARTY_NOTICES.txt
```

Recommended contents:

- Python
- PyInstaller
- tkinterdnd2
- FFmpeg
- any bundled runtime dependencies

License considerations:

- include package names, versions, source URLs, and license names
- update notices whenever dependencies change

### Screenshots

Status:

- Required: no
- Optional: yes
- Missing: yes

Recommended location:

```text
docs/images/
```

Recommended screenshots:

- main window with no video selected
- selected video state
- successful export state
- settings window

License considerations:

- use test videos or mock file names
- do not expose private file paths
- do not show copyrighted video frames unless permitted

### README Images

Status:

- Required: no
- Optional: yes
- Missing: yes

Recommended source:

- sanitized screenshots from release candidate
- simple product images created specifically for the README

License considerations:

- images must be original or explicitly licensed
- avoid official game logos or art unless permission is confirmed

### GitHub Release Description

Status:

- Required: yes
- Missing: yes

Recommended contents:

- release name
- version
- short product summary
- included features
- known limitations
- installation steps
- FFmpeg notes
- unsigned build notice if applicable
- checksums

License considerations:

- mention bundled FFmpeg and license notices
- disclose if binaries are unsigned

### Version File

Status:

- Required: yes
- Missing: yes

Recommended source:

- one canonical project version file

Recommended value for first public release:

```text
1.0.0
```

License considerations:

- none

Consistency requirements:

- About dialog
- release ZIP name
- Git tag
- GitHub release title
- CHANGELOG
- README

### CHANGELOG

Status:

- Required: yes
- Missing: yes

Recommended location:

```text
CHANGELOG.md
```

Recommended sections:

- Added
- Changed
- Fixed
- Known limitations

License considerations:

- none

### Release ZIP Contents

Status:

- Required: yes
- Missing: yes

Expected layout:

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

Must include:

- executable
- bundled runtime files
- FFmpeg and FFprobe binaries
- license files
- third-party notices
- short user README
- changelog

Must exclude:

- `.git/`
- `__pycache__/`
- source videos
- exported videos
- local settings
- export history
- development workspace files
- temporary build caches

License considerations:

- bundled binary licenses must be present inside the ZIP
- release notes should point users to included notices

## Remaining Work

- Decide project license.
- Add application icon.
- Select FFmpeg distribution.
- Add FFmpeg and FFprobe binaries.
- Add license files.
- Add third-party notices.
- Add canonical version file.
- Add CHANGELOG.
- Capture sanitized screenshots.
- Prepare GitHub release description.
- Assemble release ZIP after packaged runtime validation passes.
