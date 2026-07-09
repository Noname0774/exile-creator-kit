# Repository Review

Final repository review before the first public GitHub release.

## Summary

Repository status:

- Git working tree: clean
- Version: `v1.0.0`
- Packaging configuration: present
- FFmpeg binaries: present under `vendor/ffmpeg`
- Build artifacts: present locally but ignored
- Release ZIP: not present
- Runtime validation evidence: not complete
- License notices for FFmpeg and third-party dependencies: not present

Release decision:

```text
No-Go
```

The repository is close, but public release should wait until generated artifacts are cleaned, license notices are completed, and the packaged build passes runtime validation.

## Files To Remove

Remove from the local workspace before release packaging:

```text
build/
dist/
```

Reason:

- generated PyInstaller output
- ignored by `.gitignore`
- should be recreated from source during release build
- stale artifacts can hide packaging issues

Do not include in GitHub source release:

```text
exile-creator-kit.code-workspace
```

Reason:

- local editor workspace file
- ignored by `.gitignore`
- not needed by users

Exclude from release ZIP:

```text
.git/
build/
dist/
__pycache__/
*.pyc
*.log
settings.json
export_history.json
source videos
exported videos
```

## Files To Keep

Keep in the repository:

```text
README.md
LICENSE
CHANGELOG.md
VERSION
requirements.txt
.gitignore
```

Keep source directories:

```text
core/
gui/
tools/
packaging/
docs/
scripts/
```

Keep tracked release binaries only if legal notices are completed:

```text
vendor/ffmpeg/ffmpeg.exe
vendor/ffmpeg/ffprobe.exe
```

Required condition:

- FFmpeg license notice must be added.
- FFmpeg redistribution terms must be confirmed.
- Third-party notices must include FFmpeg.

## Final Repository Structure

Recommended public source repository:

```text
exile-creator-kit/
|
+-- README.md
+-- LICENSE
+-- CHANGELOG.md
+-- VERSION
+-- requirements.txt
+-- .gitignore
|
+-- core/
|   +-- export/
|   +-- media/
|   +-- settings/
|   +-- storage/
|
+-- gui/
|   +-- main_window.py
|   +-- settings_window.py
|   +-- about_window.py
|
+-- tools/
|   +-- export_to_x.py
|   +-- export_to_youtube.py
|   +-- validate_media_inspector.py
|   +-- *.bat
|
+-- packaging/
|   +-- pyinstaller.spec
|
+-- vendor/
|   +-- ffmpeg/
|       +-- ffmpeg.exe
|       +-- ffprobe.exe
|
+-- docs/
|   +-- ARCHITECTURE.md
|   +-- BUILD_GUIDE.md
|   +-- CURRENT_SPEC.md
|   +-- DATA_STORAGE.md
|   +-- PACKAGING.md
|   +-- RELEASE_ASSETS.md
|   +-- RELEASE_CHECKLIST.md
|   +-- RELEASE_PLAN.md
|   +-- RUNTIME_VALIDATION.md
|   +-- V1_MASTER_PLAN.md
|   +-- REPOSITORY_REVIEW.md
|
+-- scripts/
```

Required before public release:

```text
LICENSES/
|
+-- ExileCreatorKit.txt
+-- FFmpeg.txt
+-- THIRD_PARTY_NOTICES.txt
```

Optional before public release:

```text
assets/
|   +-- icons/
|       +-- exile-creator-kit.ico
|
docs/images/
    +-- main-window.png
    +-- selected-video.png
    +-- export-completed.png
    +-- settings-window.png
```

## Ignored Files Review

Current ignored patterns are appropriate for:

- build output
- logs
- editor files
- temporary files
- source videos
- exported videos
- generated audio

Confirmed ignored local files:

```text
build/
dist/
exile-creator-kit.code-workspace
```

No change required before release unless the project decides to track workspace or build output, which is not recommended.

## Build Artifacts Review

Local build artifacts exist:

```text
build/
dist/
```

These should be deleted locally before creating the final release build.

Release build should be regenerated from:

```text
packaging/pyinstaller.spec
```

Expected release output:

```text
dist/ExileCreatorKit/
|
+-- ExileCreatorKit.exe
+-- ffmpeg.exe or _internal/ffmpeg.exe
+-- ffprobe.exe or _internal/ffprobe.exe
+-- _internal/
```

The exact FFmpeg placement must match runtime lookup and release documentation.

## Public Release Checklist

### Repository

- [ ] Working tree is clean.
- [ ] `VERSION` is `v1.0.0`.
- [ ] README matches v1.0 workflow.
- [ ] CHANGELOG has v1.0 release date.
- [ ] LICENSE has final copyright holder.
- [ ] No generated files are staged.
- [ ] No local videos are staged.

### Legal

- [ ] FFmpeg redistribution terms confirmed.
- [ ] `LICENSES/FFmpeg.txt` added.
- [ ] `LICENSES/THIRD_PARTY_NOTICES.txt` added.
- [ ] Application license notice included in release ZIP.

### Packaging

- [ ] Delete stale `build/` and `dist/`.
- [ ] Rebuild with PyInstaller.
- [ ] Confirm `VERSION` is bundled.
- [ ] Confirm FFmpeg is discoverable by packaged app.
- [ ] Confirm FFprobe is discoverable by packaged app.
- [ ] Confirm packaged GUI does not rely on a source checkout.

### Runtime Validation

- [ ] Launch packaged app from Explorer.
- [ ] Launch packaged app from Command Prompt.
- [ ] Launch from a folder path containing spaces.
- [ ] Open About dialog and verify `v1.0.0`.
- [ ] Open Settings window.
- [ ] Select a supported video.
- [ ] Drop a supported video.
- [ ] Verify MediaInfo display.
- [ ] Export for X.
- [ ] Export for YouTube.
- [ ] Verify output files are playable.
- [ ] Verify settings are stored in AppData.
- [ ] Verify export history is stored in AppData.

### GitHub Release

- [ ] Create final release commit.
- [ ] Create tag `v1.0.0`.
- [ ] Create portable release ZIP.
- [ ] Generate SHA256 checksum.
- [ ] Draft GitHub Release notes.
- [ ] Attach ZIP and checksum.
- [ ] Attach screenshots if ready.
- [ ] Publish only after validation passes.

## Go / No-Go

Current decision:

```text
No-Go
```

Blocking items:

- Stale local build artifacts exist and should be regenerated.
- FFmpeg and third-party legal notices are missing.
- Runtime validation for the latest PyInstaller-compatible changes is not complete.
- Release ZIP and checksum have not been created.
- CHANGELOG still needs final release date.
- LICENSE still needs final copyright holder.

## Final Recommendations

1. Remove local `build/` and `dist/`.
2. Add `LICENSES/FFmpeg.txt`.
3. Add `LICENSES/THIRD_PARTY_NOTICES.txt`.
4. Replace copyright placeholder in `LICENSE`.
5. Rebuild using `packaging/pyinstaller.spec`.
6. Run full packaged runtime validation.
7. Create release ZIP and checksum.
8. Update CHANGELOG release date.
9. Create final release commit and tag.
10. Publish GitHub Release only after all checklist items pass.
