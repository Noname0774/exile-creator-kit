"""Export history models."""

import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path

from core.storage.path_resolver import app_data_file, migrate_legacy_json_file

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class HistoryEntry:
    input_path: str
    output_path: str
    target: str
    status: str
    timestamp: str


class ExportHistory:
    MAX_ENTRIES = 100

    def __init__(self, file_path: str | Path | None = None) -> None:
        if file_path is None:
            self._file_path = app_data_file("export_history.json")
            migrate_legacy_json_file(self._file_path, "export_history.json", list)
        else:
            self._file_path = Path(file_path)
        self._entries: list[HistoryEntry] = self._load()

    def add(self, entry: HistoryEntry) -> None:
        self._entries.append(entry)
        self._entries = self._entries[-self.MAX_ENTRIES :]
        self._save()

    def latest(self) -> HistoryEntry | None:
        if not self._entries:
            return None

        return self._entries[-1]

    def entries(self) -> tuple[HistoryEntry, ...]:
        return tuple(self._entries)

    def clear(self) -> None:
        self._entries.clear()
        self._save()

    def _load(self) -> list[HistoryEntry]:
        if self._file_path is None:
            logger.warning("Export history storage unavailable. Using empty history.")
            return []

        if not self._file_path.exists():
            return []

        try:
            with self._file_path.open("r", encoding="utf-8") as history_file:
                data = json.load(history_file)
        except (OSError, json.JSONDecodeError):
            logger.warning("Failed to load export history. Using empty history.")
            return []

        if not isinstance(data, list):
            logger.warning("Export history file is not a JSON list. Using empty history.")
            return []

        entries: list[HistoryEntry] = []
        for item in data[-self.MAX_ENTRIES :]:
            if not isinstance(item, dict):
                continue

            try:
                entries.append(
                    HistoryEntry(
                        input_path=str(item.get("input_path", "")),
                        output_path=str(item.get("output_path", "")),
                        target=str(item.get("target", "")),
                        status=str(item.get("status", "")),
                        timestamp=str(item.get("timestamp", "")),
                    )
                )
            except TypeError:
                logger.warning("Invalid export history entry skipped.")

        return entries

    def _save(self) -> None:
        if self._file_path is None:
            logger.warning("Export history storage unavailable. Save skipped.")
            return

        try:
            self._file_path.parent.mkdir(parents=True, exist_ok=True)
            with self._file_path.open("w", encoding="utf-8") as history_file:
                json.dump(
                    [asdict(entry) for entry in self._entries[-self.MAX_ENTRIES :]],
                    history_file,
                    indent=2,
                )
        except OSError:
            logger.warning("Failed to save export history.", exc_info=True)
