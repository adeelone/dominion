from __future__ import annotations

from dataclasses import dataclass

from backend.app.simulation.chronicle_log import ChronicleLog
from backend.app.simulation.models import EventKind, MagicTier, World


@dataclass(frozen=True)
class DecreeResult:
    accepted: bool
    explanation: str
    cost_credits: int


class DecreeService:
    def __init__(self) -> None:
        self.log = ChronicleLog()

    def issue(self, world: World, polity_id: str, text: str) -> DecreeResult:
        lowered = text.lower()
        if "laser" in lowered and world.logic.magic_tier not in {MagicTier.SCI_FI, MagicTier.HIGH_MAGIC}:
            return DecreeResult(False, "The decree conflicts with this world's tech and magic rules.", 1)
        treasury_delta = -8 if any(word in lowered for word in ("build", "raise", "found")) else 0
        army_delta = 5 if "raise" in lowered and "army" in lowered else 0
        self.log.append(
            world,
            kind=EventKind.DECREE,
            actor=polity_id,
            text=text,
            payload={"polity_id": polity_id, "treasury_delta": treasury_delta, "army_delta": army_delta},
        )
        return DecreeResult(True, "The decree is grounded and entered into the chronicle.", 2)
