from __future__ import annotations

from backend.app.simulation.chronicle_log import ChronicleLog
from backend.app.simulation.models import World


class Chancellor:
    def __init__(self) -> None:
        self.log = ChronicleLog()

    def brief(self, world: World) -> str:
        context = self.log.prompt_context(world)
        polities = ", ".join(str(p["name"]) for p in context["polities"])
        settlements = ", ".join(str(s["name"]) for s in context["settlements"])
        return (
            f"{world.name}: watch treasury pressure, settlement food, and rival movement. "
            f"Polities: {polities}. Settlements: {settlements}."
        )
