from backend.app.providence.grounding_engine import GroundingEngine
from backend.app.simulation.models import MagicTier
from backend.app.simulation.state_projection import StateProjection
from backend.app.worldgen.presets import demo_world


def test_dragon_materializes_as_entity_in_high_magic_world() -> None:
    world = demo_world()
    effect = GroundingEngine().resolve(world, "s1", "summon a dragon in the mountains")
    assert effect.materialized_effect["type"] == "entity"
    assert effect.materialized_effect["behavior"] == "territorial predator"


def test_dragon_reinterprets_in_low_magic_world() -> None:
    world = demo_world()
    world.logic = type(world.logic)(
        magic_tier=MagicTier.LOW_MAGIC,
        tech_era=world.logic.tech_era,
        briefing=world.logic.briefing,
        allowed_entities=(),
    )
    effect = GroundingEngine().resolve(world, "s1", "summon a dragon")
    assert effect.plausibility == "reinterpreted_low_magic"
    assert effect.materialized_effect["type"] == "phenomenon"


def test_first_order_consequence_changes_next_projection() -> None:
    world = demo_world()
    before = world.settlements["s1"].happiness
    GroundingEngine().resolve(world, "s1", "summon a dragon")
    projected = StateProjection().project(world)
    assert projected.settlements["s1"].happiness < before


def test_world_breaking_technology_declined() -> None:
    world = demo_world()
    effect = GroundingEngine().resolve(world, "s1", "give them a spaceship")
    assert effect.plausibility == "declined_world_breaking"
    assert effect.materialized_effect["type"] == "none"
