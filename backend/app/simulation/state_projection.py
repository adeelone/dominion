from __future__ import annotations

from dataclasses import replace

from .models import EventKind, Settlement, World


def _as_int(value: object, default: int = 0) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return default
    return default


class StateProjection:
    def project(self, world: World) -> World:
        projected = World(
            id=world.id,
            name=world.name,
            logic=world.logic,
            regions=world.regions.copy(),
            polities=world.polities.copy(),
            settlements=world.settlements.copy(),
            chronicle=list(world.chronicle),
            tick=world.tick,
            branch_of=world.branch_of,
        )
        for event in projected.chronicle:
            if event.kind in {EventKind.BLESSING, EventKind.CURSE, EventKind.DISASTER, EventKind.DIVINE_ACT}:
                self._apply_settlement_effect(projected, event.payload)
            if event.kind == EventKind.DECREE:
                self._apply_decree(projected, event.payload)
        return projected

    def _apply_settlement_effect(self, world: World, payload: dict[str, object]) -> None:
        settlement_id = str(payload.get("settlement_id", ""))
        settlement = world.settlements.get(settlement_id)
        if settlement is None:
            return
        deltas = payload.get("deltas", {})
        if not isinstance(deltas, dict):
            return
        world.settlements[settlement_id] = self._with_deltas(settlement, deltas)

    def _apply_decree(self, world: World, payload: dict[str, object]) -> None:
        polity_id = str(payload.get("polity_id", ""))
        polity = world.polities.get(polity_id)
        if polity is None:
            return
        treasury_delta = _as_int(payload.get("treasury_delta", 0))
        army_delta = _as_int(payload.get("army_delta", 0))
        world.polities[polity_id] = replace(
            polity,
            treasury=max(0, polity.treasury + treasury_delta),
            army_strength=max(0, polity.army_strength + army_delta),
        )

    def _with_deltas(self, settlement: Settlement, deltas: dict[object, object]) -> Settlement:
        return replace(
            settlement,
            population=max(0, settlement.population + _as_int(deltas.get("population", 0))),
            happiness=max(0, min(100, settlement.happiness + _as_int(deltas.get("happiness", 0)))),
            food=max(0, settlement.food + _as_int(deltas.get("food", 0))),
            culture=max(0, settlement.culture + _as_int(deltas.get("culture", 0))),
        )
