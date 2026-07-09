# Release Publishing

This document defines the final manual publishing steps for Exile Creator Kit v1.0.

## Checksum Generation

Generate a SHA256 checksum after creating the final release ZIP.

Expected release artifact:

```text
ExileCreatorKit-v1.0.0-win64.zip
```

PowerShell command:

```powershell
Get-FileHash .\ExileCreatorKit-v1.0.0-win64.zip -Algorithm SHA256 |
    Format-List
```

Create `SHA256SUMS.txt`:

```powershell
$hash = Get-FileHash .\ExileCreatorKit-v1.0.0-win64.zip -Algorithm SHA256
"$($hash.Hash)  ExileCreatorKit-v1.0.0-win64.zip" | Set-Content -Encoding ASCII .\SHA256SUMS.txt
```

Verify checksum:

```powershell
Get-Content .\SHA256SUMS.txt
Get-FileHash .\ExileCreatorKit-v1.0.0-win64.zip -Algorithm SHA256
```

## Git Tag Instructions

Run only after:

- final release commit is complete
- runtime validation has passed
- release ZIP has been created
- checksum has been generated
- working tree is clean

Check status:

```powershell
git status --short --branch
```

Create annotated tag:

```powershell
git tag -a v1.0.0 -m "Exile Creator Kit v1.0.0"
```

Verify tag:

```powershell
git show v1.0.0
```

Push tag:

```powershell
git push origin v1.0.0
```

Do not push the tag until the release artifact is final.

## GitHub Release Publishing Checklist

### Before Drafting

- [ ] `VERSION` is `v1.0.0`.
- [ ] About dialog shows `v1.0.0`.
- [ ] CHANGELOG has final v1.0.0 notes and release date.
- [ ] LICENSE has final copyright holder.
- [ ] `LICENSES/FFmpeg.txt` is complete.
- [ ] `LICENSES/THIRD_PARTY_NOTICES.txt` is complete.
- [ ] FFmpeg redistribution terms are confirmed.
- [ ] Build output was generated from a clean workspace.
- [ ] Runtime validation passed.

### Required Artifacts

- [ ] `ExileCreatorKit-v1.0.0-win64.zip`
- [ ] `SHA256SUMS.txt`

Optional artifacts:

- [ ] screenshots
- [ ] short demo GIF or video

### GitHub Release Fields

Release title:

```text
Exile Creator Kit v1.0.0
```

Tag:

```text
v1.0.0
```

Release type:

- Mark as latest release.
- Do not mark as pre-release if v1.0 validation has passed.
- Mark as pre-release only if validation is incomplete.

### Release Description

Use `docs/RELEASE_PLAN.md` as the source for release notes.

Must include:

- short app summary
- included features
- installation steps
- known limitations
- AppData storage note
- FFmpeg/FFprobe bundling note
- unsigned build notice if code signing is not complete
- checksum verification note

### After Publishing

- [ ] Download the ZIP from GitHub Release.
- [ ] Verify checksum from downloaded ZIP.
- [ ] Extract to a clean folder.
- [ ] Launch `ExileCreatorKit.exe`.
- [ ] Confirm About dialog version.
- [ ] Run one X export.
- [ ] Run one YouTube export.
- [ ] Verify release page links and attached files.

## No-Go Conditions

Do not publish if any of these are true:

- FFmpeg license obligations are unresolved.
- Runtime validation has not passed.
- Release ZIP is missing.
- Checksum is missing.
- `VERSION`, tag, release title, and CHANGELOG do not match.
- The packaged app cannot find FFmpeg or FFprobe.
- The packaged app depends on a source checkout.
