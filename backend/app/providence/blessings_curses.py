from __future__ import annotations

from backend.app.simulation.chronicle_log import ChronicleLog
from backend.app.simulation.models import EventKind, World


MAX_MAGNITUDE = 12


class BlessingCurseService:
    def __init__(self) -> None:
        self.log = ChronicleLog()

    def apply(self, world: World, settlement_id: str, attribute: str, magnitude: int, blessing: bool) -> None:
        bounded = max(1, min(MAX_MAGNITUDE, abs(magnitude)))
        signed = bounded if blessing else -bounded
        allowed = {"fertility": "food", "morale": "happiness", "learning": "culture", "health": "population"}
        target = allowed.get(attribute, "happiness")
        self.log.append(
            world,
            kind=EventKind.BLESSING if blessing else EventKind.CURSE,
            actor="providence",
            text=f"{'Bless' if blessing else 'Curse'} {attribute} by {bounded}.",
            payload={
                "settlement_id": settlement_id,
                "attribute": attribute,
                "duration_days": 30,
                "decay_per_week": 1,
                "deltas": {target: signed},
            },
        )
