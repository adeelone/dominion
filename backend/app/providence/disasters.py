from __future__ import annotations

from backend.app.simulation.chronicle_log import ChronicleLog
from backend.app.simulation.models import EventKind, World


DISASTER_EFFECTS = {
    "earthquake": {"population": -8, "happiness": -10, "food": -6},
    "plague": {"population": -12, "happiness": -8},
    "drought": {"food": -15, "happiness": -6},
    "storm": {"food": -5, "happiness": -4},
    "wildfire": {"food": -8, "happiness": -7},
    "flood": {"food": -6, "happiness": -5},
}


class DisasterService:
    def __init__(self) -> None:
        self.log = ChronicleLog()

    def invoke(self, world: World, settlement_id: str, kind: str) -> None:
        if kind not in DISASTER_EFFECTS:
            raise ValueError(f"Unknown disaster type: {kind}")
        self.log.append(
            world,
            kind=EventKind.DISASTER,
            actor="providence",
            text=f"A {kind} strikes.",
            payload={"settlement_id": settlement_id, "disaster": kind, "deltas": DISASTER_EFFECTS[kind]},
        )
