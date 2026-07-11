from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


@dataclass(frozen=True)
class PublishedWorld:
    id: str
    source_world_id: str
    creator_id: str
    title: str
    version: int
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class CommunityHub:
    def publish(self, source_world_id: str, creator_id: str, title: str) -> PublishedWorld:
        return PublishedWorld(str(uuid4()), source_world_id, creator_id, title, 1)

    def copy(self, publication: PublishedWorld, creator_id: str) -> PublishedWorld:
        return PublishedWorld(str(uuid4()), publication.source_world_id, creator_id, f"{publication.title} Copy", 1)
