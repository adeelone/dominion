from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorldMindResponse:
    text: str
    tokens_in: int
    tokens_out: int
    cost_credits: int


class WorldMind:
    def complete(self, purpose: str, prompt: str, tier: str = "fast") -> WorldMindResponse:
        cost = 1 if tier == "fast" else 5
        return WorldMindResponse(
            text=f"[fixture:{purpose}:{tier}] {prompt[:160]}",
            tokens_in=len(prompt.split()),
            tokens_out=16,
            cost_credits=cost,
        )
