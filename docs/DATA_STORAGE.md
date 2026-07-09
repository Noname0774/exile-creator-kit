# Application Data Storage

This document defines the single storage location for Exile Creator Kit application data.

The storage location must be stable regardless of how the application is launched.

## Current Implementation

Current data files use relative paths:

```text
settings.json
export_history.json
```

This means the files are written to the current working directory.

That can change depending on whether the app is launched from:

- VS Code
- Command Prompt
- Explorer
- an installed application shortcut

This is not acceptable for v1.0.

## Storage Location

Use the standard Windows roaming application data directory:

```text
%APPDATA%\Exile Creator Kit
```

Typical expanded path:

```text
C:\Users\<user>\AppData\Roaming\Exile Creator Kit
```

## Directory Layout

```text
%APPDATA%\Exile Creator Kit
|
+-- settings.json
+-- export_history.json
```

## File Responsibilities

### settings.json

Stores user settings.

Examples:

- default output folder
- last selected folder
- export preset settings
- FFmpeg path
- FFprobe path

### export_history.json

Stores recent export history.

Rules:

- store completed exports
- store failed exports
- keep latest 100 entries
- do not store source video data
- do not store generated video data

## Migration Strategy

On startup:

1. Resolve the application data directory.
2. Create the directory if it does not exist.
3. Check for existing files in the new location.
4. If a new-location file exists, use it.
5. If a new-location file does not exist, check the legacy relative file.
6. If a legacy file exists and is valid, copy or move it to the new location.
7. Load from the new location.
8. If migration fails, log the error and continue with defaults.

Legacy files:

```text
settings.json
export_history.json
```

Legacy files should not be required after migration.

## Fallback Behavior

If `%APPDATA%` is available:

- use `%APPDATA%\Exile Creator Kit`

If `%APPDATA%` is unavailable:

- fall back to the user's home directory:

```text
~\.exile-creator-kit
```

If neither location can be created:

- keep application startup alive
- use in-memory defaults
- show user-friendly errors when save is required
- log the failure

The application must not crash because application data storage is unavailable.

## Release Implications

Before v1.0 release:

- `settings.json` must no longer be cwd-dependent.
- `export_history.json` must no longer be cwd-dependent.
- release validation must verify startup from VS Code.
- release validation must verify startup from Command Prompt.
- release validation must verify startup from Explorer.
- release validation must verify installed-app startup when packaging exists.
- migration from legacy relative files must be tested.
- corrupted data files must not block startup.

## Implementation Plan

### Step 1: Add App Data Path Resolution

Create a shared path resolver for application data.

Required behavior:

- resolve `%APPDATA%\Exile Creator Kit`
- create the directory if needed
- provide file paths for `settings.json` and `export_history.json`
- fall back to `~\.exile-creator-kit` if needed

### Step 2: Update SettingsRepository

Change the default settings path from:

```text
settings.json
```

to:

```text
%APPDATA%\Exile Creator Kit\settings.json
```

Keep constructor override support for tests and future tools.

### Step 3: Update ExportHistory

Change the default history path from:

```text
export_history.json
```

to:

```text
%APPDATA%\Exile Creator Kit\export_history.json
```

Keep constructor override support for tests and future tools.

### Step 4: Add Migration

When the new file does not exist:

- check for legacy relative file
- copy valid legacy data to the new location
- log migration result
- continue safely on failure

### Step 5: Validate Launch Methods

Validate that both files are read and written to the same location when launched from:

- VS Code
- Command Prompt
- Explorer
- installed application

## Key Decision

All application data must live under:

```text
%APPDATA%\Exile Creator Kit
```

Relative data files in the working directory are legacy only and should not be used as the active storage location after migration.
