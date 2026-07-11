from __future__ import annotations

from dataclasses import dataclass

from .chronicle_log import ChronicleLog
from .models import EventKind, World


@dataclass(frozen=True)
class ArchiveResult:
    compressed_count: int
    summary: str | None


class ArchiveEngine:
    def __init__(self, threshold: int = 12) -> None:
        self.threshold = threshold
        self.log = ChronicleLog()

    def maybe_compress(self, world: World) -> ArchiveResult:
        raw_events = [event for event in world.chronicle if event.kind != EventKind.ARCHIVE_SUMMARY]
        if len(raw_events) < self.threshold:
            return ArchiveResult(compressed_count=0, summary=None)
        chunk = raw_events[: self.threshold]
        summary = "; ".join(f"{event.tick}:{event.kind.value}:{event.text}" for event in chunk)
        self.log.append(
            world,
            kind=EventKind.ARCHIVE_SUMMARY,
            actor="archive-engine",
            text=f"Compressed {len(chunk)} old events into durable history.",
            payload={"raw_event_ids": [event.id for event in chunk], "summary": summary},
        )
        return ArchiveResult(compressed_count=len(chunk), summary=summary)
