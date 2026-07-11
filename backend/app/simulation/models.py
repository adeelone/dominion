from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from uuid import uuid4


class MagicTier(str, Enum):
    HISTORICAL = "historical"
    LOW_MAGIC = "low_magic"
    HIGH_MAGIC = "high_magic"
    SCI_FI = "sci_fi"


class EventKind(str, Enum):
    DECREE = "decree"
    DIPLOMACY = "diplomacy"
    DIVINE_ACT = "divine_act"
    BLESSING = "blessing"
    CURSE = "curse"
    DISASTER = "disaster"
    OMEN = "omen"
    WORLD_EVENT = "world_event"
    ARCHIVE_SUMMARY = "archive_summary"


@dataclass(frozen=True)
class Region:
    id: str
    name: str
    biome: str
    tags: tuple[str, ...] = ()
    points: tuple[tuple[float, float], ...] = ()


@dataclass(frozen=True)
class Polity:
    id: str
    name: str
    region_ids: tuple[str, ...]
    tags: tuple[str, ...] = ()
    treasury: int = 100
    army_strength: int = 10


@dataclass(frozen=True)
class Settlement:
    id: str
    name: str
    region_id: str
    population: int
    happiness: int
    food: int
    culture: int
    tags: tuple[str, ...] = ()


@dataclass(frozen=True)
class WorldLogic:
    magic_tier: MagicTier
    tech_era: str
    briefing: str
    allowed_entities: tuple[str, ...] = ()


@dataclass(frozen=True)
class ChronicleEvent:
    id: str
    world_id: str
    tick: int
    kind: EventKind
    actor: str
    text: str
    payload: dict[str, object]
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        world_id: str,
        tick: int,
        kind: EventKind,
        actor: str,
        text: str,
        payload: dict[str, object] | None = None,
    ) -> ChronicleEvent:
        return cls(
            id=str(uuid4()),
            world_id=world_id,
            tick=tick,
            kind=kind,
            actor=actor,
            text=text,
            payload=payload or {},
        )


@dataclass
class World:
    id: str
    name: str
    logic: WorldLogic
    regions: dict[str, Region]
    polities: dict[str, Polity]
    settlements: dict[str, Settlement]
    chronicle: list[ChronicleEvent] = field(default_factory=list)
    tick: int = 0
    branch_of: str | None = None
