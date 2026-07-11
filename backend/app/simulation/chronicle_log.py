from __future__ import annotations

from .models import ChronicleEvent, EventKind, World


class ChronicleLog:
    """Append-only source of truth for every world mutation."""

    def append(
        self,
        world: World,
        *,
        kind: EventKind,
        actor: str,
        text: str,
        payload: dict[str, object] | None = None,
    ) -> ChronicleEvent:
        event = ChronicleEvent.create(
            world_id=world.id,
            tick=world.tick,
            kind=kind,
            actor=actor,
            text=text,
            payload=payload,
        )
        world.chronicle.append(event)
        return event

    def prompt_context(self, world: World) -> dict[str, object]:
        return {
            "world": world.name,
            "logic": world.logic,
            "polities": [
                {"name": p.name, "tags": p.tags, "treasury": p.treasury, "army": p.army_strength}
                for p in world.polities.values()
            ],
            "settlements": [
                {
                    "name": s.name,
                    "tags": s.tags,
                    "population": s.population,
                    "happiness": s.happiness,
                    "food": s.food,
                }
                for s in world.settlements.values()
            ],
        }
