# Release Checklist

Use this checklist for every Exile Creator Kit release.

## Versioning

- [ ] Confirm the release version.
- [ ] Update visible application version text.
- [ ] Confirm version naming matches the release type.
- [ ] Confirm release branch or commit is correct.

## Build

- [ ] Start from a clean working tree or clearly documented release branch.
- [ ] Confirm the application starts successfully.
- [ ] Confirm no release-only files are missing.
- [ ] Confirm generated or temporary files are not included.

## Dependencies

- [ ] Confirm Python version requirement.
- [ ] Confirm FFmpeg is installed and available.
- [ ] Confirm FFprobe is installed and available.
- [ ] Confirm GUI dependencies are installed.
- [ ] Confirm `requirements.txt` is current.

## Runtime Validation

- [ ] Launch the main application.
- [ ] Open the Settings window.
- [ ] Open the About dialog.
- [ ] Select a supported video file.
- [ ] Drop a supported video file into the GUI.
- [ ] Confirm unsupported files are rejected clearly.

## GUI Validation

- [ ] Confirm first launch screen is understandable.
- [ ] Confirm selected video information is readable.
- [ ] Confirm export buttons are clear.
- [ ] Confirm progress state changes are visible.
- [ ] Confirm success and failure messages are human-readable.
- [ ] Confirm Recent Exports updates after export.

## Export Validation

- [ ] Export a video for X.
- [ ] Export a video for YouTube.
- [ ] Confirm output filenames are correct.
- [ ] Confirm output files are playable.
- [ ] Confirm output path is shown after export.
- [ ] Confirm Open Output Folder works.

## Settings Validation

- [ ] Save General settings.
- [ ] Relaunch the application.
- [ ] Confirm last selected folder is remembered when enabled.
- [ ] Confirm last selected folder is not remembered when disabled.
- [ ] Confirm default output folder is used when configured.
- [ ] Confirm default output folder fallback works when not configured.

## Packaging

- [ ] Confirm release package includes required source files.
- [ ] Confirm release package excludes source videos.
- [ ] Confirm release package excludes generated output videos.
- [ ] Confirm release package excludes local settings when appropriate.
- [ ] Confirm installation or launch instructions are included.

## Release Notes

- [ ] Summarize user-facing changes.
- [ ] Summarize known limitations.
- [ ] Mention dependency requirements.
- [ ] Mention migration notes if settings changed.
- [ ] Mention validation status.

## Git Tag

- [ ] Confirm release commit.
- [ ] Create the version tag.
- [ ] Verify the tag points to the correct commit.
- [ ] Push the tag when ready.

## GitHub Release

- [ ] Create the GitHub release from the tag.
- [ ] Add release notes.
- [ ] Attach release artifacts if applicable.
- [ ] Mark pre-release status when appropriate.
- [ ] Verify the published release page.
