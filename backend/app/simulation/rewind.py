from __future__ import annotations

from uuid import uuid4

from .models import World


class RewindService:
    def fork_at_event(self, world: World, event_id: str) -> World:
        index = next((i for i, event in enumerate(world.chronicle) if event.id == event_id), None)
        if index is None:
            raise ValueError(f"Event {event_id} does not exist in world {world.id}.")
        retained = world.chronicle[: index + 1]
        return World(
            id=str(uuid4()),
            name=f"{world.name} Fork",
            logic=world.logic,
            regions=world.regions.copy(),
            polities=world.polities.copy(),
            settlements=world.settlements.copy(),
            chronicle=list(retained),
            tick=retained[-1].tick if retained else 0,
            branch_of=world.id,
        )
