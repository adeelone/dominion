from __future__ import annotations

from backend.app.simulation.chronicle_log import ChronicleLog
from backend.app.simulation.models import EventKind, World


class OmenService:
    def __init__(self) -> None:
        self.log = ChronicleLog()

    def send(self, world: World, settlement_id: str, tone: str) -> None:
        delta = 2 if tone == "favorable" else -2
        self.log.append(
            world,
            kind=EventKind.OMEN,
            actor="providence",
            text=f"A {tone} omen spreads through the settlement.",
            payload={"settlement_id": settlement_id, "deltas": {"happiness": delta}},
        )
