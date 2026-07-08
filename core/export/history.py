"""Export history models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class HistoryEntry:
    input_path: str
    output_path: str
    target: str
    status: str
    timestamp: str


class ExportHistory:
    def __init__(self) -> None:
        self._entries: list[HistoryEntry] = []

    def add(self, entry: HistoryEntry) -> None:
        self._entries.append(entry)

    def latest(self) -> HistoryEntry | None:
        if not self._entries:
            return None

        return self._entries[-1]

    def clear(self) -> None:
        self._entries.clear()
