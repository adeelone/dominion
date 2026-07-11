from __future__ import annotations

from dataclasses import replace

from backend.app.simulation.models import MagicTier, Region, World, WorldLogic


class WorldForge:
    def update_logic(self, world: World, *, magic_tier: MagicTier, tech_era: str, briefing: str) -> World:
        world.logic = WorldLogic(magic_tier=magic_tier, tech_era=tech_era, briefing=briefing, allowed_entities=world.logic.allowed_entities)
        return world

    def tag_settlement(self, world: World, settlement_id: str, tag: str) -> None:
        settlement = world.settlements[settlement_id]
        world.settlements[settlement_id] = replace(settlement, tags=tuple(sorted(set(settlement.tags) | {tag})))

    def tag_region(self, world: World, region_id: str, tag: str) -> None:
        region = world.regions[region_id]
        world.regions[region_id] = Region(region.id, region.name, region.biome, tuple(sorted(set(region.tags) | {tag})), region.points)
