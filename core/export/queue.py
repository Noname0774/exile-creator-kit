"""Export queue models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ExportJob:
    input_path: str
    output_path: str
    target: str
    status: str


class ExportQueue:
    def __init__(self) -> None:
        self._jobs: list[ExportJob] = []

    def add(self, job: ExportJob) -> None:
        self._jobs.append(job)

    def pop(self) -> ExportJob | None:
        if self.is_empty():
            return None

        return self._jobs.pop(0)

    def clear(self) -> None:
        self._jobs.clear()

    def is_empty(self) -> bool:
        return len(self._jobs) == 0
