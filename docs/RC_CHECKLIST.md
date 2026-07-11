# v1.2.0-rc.1 Release Candidate Checklist

Use this checklist before publishing `v1.2.0-rc.1`.

## Result Legend

- Pass: Works as expected.
- Fail: Blocks release or requires a fix.
- Notes: Record environment, file names, errors, screenshots, or follow-up items.

## Checklist

| Area | Check | Pass | Fail | Notes |
| --- | --- | --- | --- | --- |
| Startup | Application launches from source. | [ ] | [ ] | |
| Startup | Application launches from packaged build. | [ ] | [ ] | |
| Startup | Main window renders without clipped controls. | [ ] | [ ] | |
| Startup | About window opens and shows the expected version. | [ ] | [ ] | |
| GPU Detection | NVIDIA GPU is detected when available. | [ ] | [ ] | |
| GPU Detection | Unknown GPU state is handled without crashing. | [ ] | [ ] | |
| GPU Detection | Available encoder list includes Software (libx264). | [ ] | [ ] | |
| Encoder Auto | Auto selects the best available encoder. | [ ] | [ ] | |
| Encoder Auto | Auto falls back to software when hardware encoding fails. | [ ] | [ ] | |
| Encoder Auto | Software fallback preference is remembered for the current session. | [ ] | [ ] | |
| Environment | OS information is detected. | [ ] | [ ] | |
| Environment | Python version is detected. | [ ] | [ ] | |
| Environment | FFmpeg version is detected. | [ ] | [ ] | |
| Environment | FFprobe version is detected. | [ ] | [ ] | |
| Environment | App version is detected. | [ ] | [ ] | |
| Diagnostics | GPU diagnostic status is correct. | [ ] | [ ] | |
| Diagnostics | Encoder diagnostic status is correct. | [ ] | [ ] | |
| Diagnostics | FFmpeg diagnostic status is correct. | [ ] | [ ] | |
| Diagnostics | FFprobe diagnostic status is correct. | [ ] | [ ] | |
| Diagnostics | Output folder diagnostic status is correct. | [ ] | [ ] | |
| Media Summary | Valid MP4 file displays media information. | [ ] | [ ] | |
| Media Summary | Valid MKV file displays media information. | [ ] | [ ] | |
| Media Summary | Valid MOV file displays media information. | [ ] | [ ] | |
| Media Summary | Valid AVI file displays media information. | [ ] | [ ] | |
| Media Summary | Invalid video shows a friendly error. | [ ] | [ ] | |
| Media Summary | Corrupted ffprobe JSON does not crash the GUI. | [ ] | [ ] | |
| Preflight | OK result starts export. | [ ] | [ ] | |
| Preflight | Warning result shows Continue / Cancel dialog. | [ ] | [ ] | |
| Preflight | Warning + Continue starts export. | [ ] | [ ] | |
| Preflight | Warning + Cancel does not start export. | [ ] | [ ] | |
| Preflight | Error result blocks export. | [ ] | [ ] | |
| Preflight | Error result displays a clear message. | [ ] | [ ] | |
| Export | X export creates an output file. | [ ] | [ ] | |
| Export | YouTube export creates an output file. | [ ] | [ ] | |
| Export | Output path displayed in GUI matches actual file path. | [ ] | [ ] | |
| Export | Export success is recorded in history. | [ ] | [ ] | |
| Export | Export failure is recorded in history. | [ ] | [ ] | |
| Export | Success log is written. | [ ] | [ ] | |
| Export | Failure log is written. | [ ] | [ ] | |
| Presets | X (512 MB) preset affects FFmpeg settings. | [ ] | [ ] | |
| Presets | YouTube (High Quality) preset affects FFmpeg settings. | [ ] | [ ] | |
| Presets | YouTube Shorts preset affects FFmpeg settings. | [ ] | [ ] | |
| Presets | Discord preset affects FFmpeg settings. | [ ] | [ ] | |
| Presets | Custom preset uses existing detailed settings. | [ ] | [ ] | |
| Presets | Selected preset is saved. | [ ] | [ ] | |
| Presets | Saved preset is restored on next launch. | [ ] | [ ] | |
| Settings | Settings window opens. | [ ] | [ ] | |
| Settings | Default Export Preset can be edited and saved. | [ ] | [ ] | |
| Settings | Default Encoder can be edited and saved. | [ ] | [ ] | |
| Settings | Output Folder can be edited and saved. | [ ] | [ ] | |
| Settings | Settings persist after restart. | [ ] | [ ] | |
| Settings | Corrupted settings.json does not prevent startup. | [ ] | [ ] | |
| UI | Premium dark theme is applied consistently. | [ ] | [ ] | |
| UI | Main window fits 900 x 780 baseline layout. | [ ] | [ ] | |
| UI | Scroll behavior works on smaller screens. | [ ] | [ ] | |
| UI | Buttons are disabled during export. | [ ] | [ ] | |
| UI | Open Output Folder button works after success. | [ ] | [ ] | |
| UI | Open Log Folder button works after failure. | [ ] | [ ] | |
| Packaging | PyInstaller spec includes required core modules. | [ ] | [ ] | |
| Packaging | FFmpeg is bundled in the expected layout. | [ ] | [ ] | |
| Packaging | FFprobe is bundled in the expected layout. | [ ] | [ ] | |
| Packaging | VERSION file is bundled. | [ ] | [ ] | |
| Packaging | Assets and icons are bundled. | [ ] | [ ] | |
| Packaging | Packaged app uses AppData storage. | [ ] | [ ] | |
| README | README version and release link are correct. | [ ] | [ ] | |
| README | README screenshot is current. | [ ] | [ ] | |
| README | README has no mojibake or broken characters. | [ ] | [ ] | |
| README | README describes v1.2.0-rc.1 scope accurately. | [ ] | [ ] | |
| Release Assets | LICENSE exists. | [ ] | [ ] | |
| Release Assets | CHANGELOG includes v1.2.0-rc.1 notes. | [ ] | [ ] | |
| Release Assets | VERSION matches v1.2.0-rc.1. | [ ] | [ ] | |
| Release Assets | FFmpeg license notice exists. | [ ] | [ ] | |
| Release Assets | Third-party notices exist. | [ ] | [ ] | |
| Release Assets | Release ZIP contents are verified. | [ ] | [ ] | |
| Release Assets | SHA256 checksum instructions are ready. | [ ] | [ ] | |
| Release Assets | Git tag plan is ready. | [ ] | [ ] | |

## Final RC Decision

| Decision | Pass | Fail | Notes |
| --- | --- | --- | --- |
| v1.2.0-rc.1 is ready for release. | [ ] | [ ] | |
