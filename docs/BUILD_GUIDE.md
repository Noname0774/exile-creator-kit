# Build Guide

This guide defines the first Windows distributable build process for Exile Creator Kit.

Do not create release artifacts until required bundled assets are present.

## Prerequisites

Required:

- Windows 10 or later
- Python 3.11 or later
- PyInstaller
- project dependencies from `requirements.txt`
- `packaging/pyinstaller.spec`

Install Python dependencies:

```powershell
python -m pip install -r requirements.txt
python -m pip install pyinstaller
```

Required before a release build:

```text
vendor/
  ffmpeg/
    ffmpeg.exe
    ffprobe.exe

assets/
  icons/
    exile-creator-kit.ico

LICENSES/
  ExileCreatorKit.txt
  FFmpeg.txt
```

Current rule:

- If `ffmpeg.exe` or `ffprobe.exe` is missing, do not create a release artifact.
- If icon or license files are missing, a local test build may be possible, but release packaging is not complete.

## Build Command

Run from the repository root:

```powershell
python -m PyInstaller --clean --noconfirm packaging\pyinstaller.spec
```

Target mode:

```text
onedir
```

The spec file controls:

- GUI entry point: `gui/main_window.py`
- application name: `ExileCreatorKit`
- bundled tools
- hidden imports
- optional icon
- optional FFmpeg and FFprobe binaries

## Expected Output Directory

PyInstaller should create:

```text
dist/
  ExileCreatorKit/
    ExileCreatorKit.exe
    ffmpeg.exe
    ffprobe.exe
    _internal/
    tools/
    assets/
    LICENSES/
```

Notes:

- `ffmpeg.exe` and `ffprobe.exe` are placed beside `ExileCreatorKit.exe`.
- AppData remains the storage location for settings and export history.
- User videos and exported videos are not bundled.

## Build Steps

1. Confirm working tree is clean.
2. Confirm `packaging/pyinstaller.spec` exists.
3. Confirm Python dependencies are installed.
4. Confirm `vendor\ffmpeg\ffmpeg.exe` exists.
5. Confirm `vendor\ffmpeg\ffprobe.exe` exists.
6. Confirm icon exists if building a release candidate.
7. Confirm license notices exist if building a release candidate.
8. Run the build command.
9. Inspect `dist\ExileCreatorKit`.
10. Run runtime verification.

## Verification Checklist

After building, verify:

- `dist\ExileCreatorKit\ExileCreatorKit.exe` exists.
- `dist\ExileCreatorKit\ffmpeg.exe` exists.
- `dist\ExileCreatorKit\ffprobe.exe` exists.
- The app starts by double-clicking `ExileCreatorKit.exe`.
- The About dialog opens.
- The Settings window opens.
- Settings are stored under `%APPDATA%\Exile Creator Kit`.
- Export history is stored under `%APPDATA%\Exile Creator Kit`.
- A supported video can be selected.
- MediaInfo is displayed.
- X export can run.
- YouTube export can run.
- Output files are created at the displayed output path.
- Open Output Folder works.
- Missing or invalid video files show friendly errors.
- The app works from a folder path containing spaces.

## Troubleshooting

### PyInstaller is not found

Install PyInstaller:

```powershell
python -m pip install pyinstaller
```

### tkinterdnd2 is missing

Install project requirements:

```powershell
python -m pip install -r requirements.txt
```

### FFmpeg or FFprobe is missing from output

Confirm these files exist before build:

```text
vendor\ffmpeg\ffmpeg.exe
vendor\ffmpeg\ffprobe.exe
```

Then rebuild with `--clean`.

### App starts but export fails

Verify:

- `ffmpeg.exe` is beside `ExileCreatorKit.exe`
- `ffprobe.exe` is beside `ExileCreatorKit.exe`
- Settings do not point to an invalid custom FFmpeg path
- The selected output folder exists and is writable

### GUI starts from source but not from build

Check:

- hidden imports in `packaging/pyinstaller.spec`
- bundled `tools/` folder
- tkinter runtime support
- tkinterdnd2 availability

### Settings or history appear in the wrong folder

Expected location:

```text
%APPDATA%\Exile Creator Kit
```

The packaged app must not use the current working directory for active settings or history.

## Release Artifact Rule

Do not create a v1.0 release ZIP until all are true:

- FFmpeg binary is present.
- FFprobe binary is present.
- FFmpeg license notice is present.
- application license notice is present.
- icon decision is complete.
- packaged runtime validation passes.

## Remaining Build Work

- Add final FFmpeg and FFprobe binaries.
- Add license notices.
- Add icon asset or decide to ship without an icon for test builds.
- Run the first PyInstaller build.
- Validate packaged runtime behavior.
- Prepare portable ZIP only after validation passes.
