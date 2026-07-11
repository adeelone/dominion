from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class WorldMindResponse:
    text: str
    tokens_in: int
    tokens_out: int
    cost_credits: int


@dataclass(frozen=True)
class WorldMindCall:
    purpose: str
    tier: str
    tokens_in: int
    tokens_out: int
    cost_credits: int
    created_at: datetime


class WorldMind:
    def __init__(self) -> None:
        self.calls: list[WorldMindCall] = []

    def complete(self, purpose: str, prompt: str, tier: str = "fast") -> WorldMindResponse:
        cost = 1 if tier == "fast" else 5
        response = WorldMindResponse(
            text=f"[fixture:{purpose}:{tier}] {prompt[:160]}",
            tokens_in=len(prompt.split()),
            tokens_out=16,
            cost_credits=cost,
        )
        self.calls.append(
            WorldMindCall(
                purpose=purpose,
                tier=tier,
                tokens_in=response.tokens_in,
                tokens_out=response.tokens_out,
                cost_credits=response.cost_credits,
                created_at=datetime.now(UTC),
            )
        )
        return response
