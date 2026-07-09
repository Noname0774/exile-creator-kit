# Runtime Validation

Use this checklist before every Exile Creator Kit release.

Each item must be tested with a real supported video file.

## GUI Startup

### Test Steps

- Start Exile Creator Kit from the normal user entry point.
- Open the main window.
- Open the About dialog.
- Close the About dialog.

### Expected Result

- The main window opens without errors.
- The application title is visible.
- The About dialog opens and closes normally.
- No Python traceback is shown.

### Pass / Fail Criteria

- Pass: The GUI starts and remains usable.
- Fail: Startup crashes, hangs, or shows a traceback.

## Settings

### Test Steps

- Open the Settings window.
- Change the default output folder.
- Toggle Open output folder after export.
- Toggle Remember last selected folder.
- Save General settings.
- Close and reopen the Settings window.

### Expected Result

- Saved values are displayed after reopening Settings.
- The main GUI continues to work after saving.
- No unrelated settings are reset.

### Pass / Fail Criteria

- Pass: Settings load, save, and reload correctly.
- Fail: Settings are lost, corrupted, or cause the GUI to fail.

## X Export

### Test Steps

- Select or drop a supported video file.
- Click Export for X.
- Wait for the export to finish.
- Locate the generated output file.
- Play the exported video.

### Expected Result

- Export enters Preparing and Encoding states.
- Export finishes as Completed.
- Output filename uses the X suffix.
- Output file is playable.
- Recent Exports records the X export.

### Pass / Fail Criteria

- Pass: X export completes and produces a playable file.
- Fail: Export fails, produces no file, or creates an unplayable file.

## YouTube Export

### Test Steps

- Select or drop a supported video file.
- Click Export for YouTube.
- Wait for the export to finish.
- Locate the generated output file.
- Play the exported video.

### Expected Result

- Export enters Preparing and Encoding states.
- Export finishes as Completed.
- Output filename uses the YouTube suffix.
- Output file is playable.
- Recent Exports records the YouTube export.

### Pass / Fail Criteria

- Pass: YouTube export completes and produces a playable file.
- Fail: Export fails, produces no file, or creates an unplayable file.

## MediaInfo

### Test Steps

- Select a supported video file.
- Review the Selected Video section.
- Repeat with at least one different supported format if available.

### Expected Result

- File name is shown.
- Location is shown.
- Duration is formatted for users.
- Resolution is shown.
- File size is shown in MB or GB.

### Pass / Fail Criteria

- Pass: Media information is readable and accurate enough for release.
- Fail: Media information is blank, misleading, or causes a crash.

## Queue

### Test Steps

- Start an export.
- Confirm export buttons are disabled while the export is running.
- Wait for the export to finish.
- Start another export.

### Expected Result

- Only one GUI export runs at a time.
- Export buttons are re-enabled after completion or failure.
- The next export can start normally.

### Pass / Fail Criteria

- Pass: Queue flow prevents duplicate concurrent exports from the GUI.
- Fail: Multiple exports start accidentally or buttons remain disabled.

## History

### Test Steps

- Complete a successful X export.
- Complete a successful YouTube export.
- Trigger one failed export using an invalid export condition.
- Review Recent Exports.

### Expected Result

- Successful exports are listed.
- Failed exports are listed.
- Each entry shows file name, target, status, and time.
- The newest entries are visible.

### Pass / Fail Criteria

- Pass: Recent Exports reflects both Completed and Failed exports.
- Fail: Failed exports are missing or entries show incorrect target/status.

## Output Path

### Test Steps

- Configure a default output folder.
- Export for X.
- Export for YouTube.
- Compare the displayed Saved to path with the actual generated file path.
- Click Open Output Folder.

### Expected Result

- Displayed path matches the actual output file location.
- History uses the same output path.
- Open Output Folder opens the folder containing the output file.

### Pass / Fail Criteria

- Pass: GUI, export result, history, and folder opening use the same path.
- Fail: Any displayed path differs from the actual generated file path.

## Error Handling

### Test Steps

- Try exporting without selecting a video.
- Try selecting an unsupported file type.
- Try running with FFmpeg unavailable or misconfigured.
- Try using a corrupted video file if available.

### Expected Result

- The GUI shows a friendly error message.
- The application does not crash.
- Failed exports are recorded when an export process was started.
- No Python traceback is shown to the user.

### Pass / Fail Criteria

- Pass: Errors are understandable and the app remains usable.
- Fail: Errors crash the app, expose tracebacks, or leave the UI stuck.

## FFmpeg Path

### Test Steps

- Use the default FFmpeg setting.
- Export a video.
- Configure a valid custom FFmpeg path.
- Export again.
- Configure a missing custom FFmpeg path.
- Try exporting again.

### Expected Result

- Default FFmpeg path works when FFmpeg is on PATH.
- Valid custom FFmpeg path is used.
- Missing custom path falls back safely or shows a friendly failure.
- The GUI does not perform direct FFmpeg lookup.

### Pass / Fail Criteria

- Pass: FFmpeg path behavior is predictable and does not crash startup.
- Fail: Custom path is ignored, missing path crashes, or GUI does direct lookup.

## Settings Migration

### Test Steps

- Start with no settings.json.
- Start with an older settings.json missing newer fields.
- Start with an invalid JSON settings file.
- Start with settings containing invalid preset values.

### Expected Result

- Missing settings file creates default behavior.
- Older settings are merged with current defaults.
- Invalid JSON is logged and defaults are used.
- Invalid preset values are rejected and default values are used.
- Application startup continues.

### Pass / Fail Criteria

- Pass: All settings migration cases start successfully.
- Fail: Any settings case prevents application startup.

## Release Decision

- Pass release validation only when every section passes.
- Record any failed section in release notes if release proceeds.
- Block v1.0 release for failures in GUI startup, export, output path, settings loading, or FFmpeg path handling.
