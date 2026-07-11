from __future__ import annotations

MODEL_COSTS = {"fast": 1, "deep": 5}


class QuotaService:
    def quote(self, tier: str, calls: int = 1) -> int:
        return MODEL_COSTS.get(tier, MODEL_COSTS["fast"]) * calls

    def can_spend(self, balance: int, tier: str, calls: int = 1) -> bool:
        return balance >= self.quote(tier, calls)
