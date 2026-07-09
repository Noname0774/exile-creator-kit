"""Application data path resolution."""

import json
import logging
import os
import shutil
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

APP_DIR_NAME = "Exile Creator Kit"
FALLBACK_DIR_NAME = ".exile-creator-kit"


def app_data_dir() -> Path | None:
    """Return the stable application data directory, creating it if possible."""
    candidates: list[Path] = []
    appdata = os.environ.get("APPDATA", "").strip()
    if appdata:
        candidates.append(Path(appdata) / APP_DIR_NAME)

    candidates.append(Path.home() / FALLBACK_DIR_NAME)

    for candidate in candidates:
        try:
            candidate.mkdir(parents=True, exist_ok=True)
        except OSError:
            logger.warning(
                "Application data directory unavailable: %s",
                candidate,
                exc_info=True,
            )
            continue

        return candidate

    logger.warning("No application data directory is available.")
    return None


def app_data_file(file_name: str) -> Path | None:
    """Return a stable application data file path."""
    directory = app_data_dir()
    if directory is None:
        return None

    return directory / file_name


def migrate_legacy_json_file(
    target_path: Path | None,
    legacy_file_name: str,
    expected_type: type[Any],
) -> None:
    """Copy a valid legacy cwd JSON file to the app data location if needed."""
    if target_path is None or target_path.exists():
        return

    legacy_path = Path(legacy_file_name)
    if not legacy_path.exists():
        return

    try:
        with legacy_path.open("r", encoding="utf-8") as legacy_file:
            data = json.load(legacy_file)
    except (OSError, json.JSONDecodeError):
        logger.warning("Legacy data migration skipped: invalid %s.", legacy_path)
        return

    if not isinstance(data, expected_type):
        logger.warning("Legacy data migration skipped: unexpected %s.", legacy_path)
        return

    try:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(legacy_path, target_path)
        logger.info("Migrated legacy data file to %s.", target_path)
    except OSError:
        logger.warning("Legacy data migration failed: %s.", legacy_path, exc_info=True)
