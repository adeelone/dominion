from __future__ import annotations

from dataclasses import dataclass

from .chronicle_log import ChronicleLog
from .models import EventKind, World


@dataclass(frozen=True)
class TickResult:
    old_tick: int
    new_tick: int
    events_created: int


class Clock:
    presets = {"day": 1, "week": 7, "month": 30, "year": 365}

    def __init__(self) -> None:
        self.log = ChronicleLog()

    def advance(self, world: World, amount: int | str) -> TickResult:
        old_tick = world.tick
        days = self.presets.get(amount, amount) if isinstance(amount, str) else amount
        if not isinstance(days, int) or days <= 0:
            raise ValueError("Clock advance requires a positive day count or known preset.")
        world.tick += days
        created = 0
        for settlement in world.settlements.values():
            if settlement.food < settlement.population // 4:
                self.log.append(
                    world,
                    kind=EventKind.WORLD_EVENT,
                    actor="nature",
                    text=f"{settlement.name} faces hunger pressure after {days} days.",
                    payload={"settlement_id": settlement.id, "deltas": {"happiness": -2}},
                )
                created += 1
        return TickResult(old_tick=old_tick, new_tick=world.tick, events_created=created)
