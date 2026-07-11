from __future__ import annotations

from backend.app.simulation.models import World


class Chancellor:
    def brief(self, world: World) -> str:
        polities = ", ".join(polity.name for polity in world.polities.values())
        settlements = ", ".join(settlement.name for settlement in world.settlements.values())
        return (
            f"{world.name}: watch treasury pressure, settlement food, and rival movement. "
            f"Polities: {polities}. Settlements: {settlements}."
        )
