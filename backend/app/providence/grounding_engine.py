from __future__ import annotations

from dataclasses import dataclass

from backend.app.simulation.chronicle_log import ChronicleLog
from backend.app.simulation.models import EventKind, MagicTier, World


@dataclass(frozen=True)
class GroundedEffect:
    parsed_intent: str
    plausibility: str
    materialized_effect: dict[str, object]
    first_consequence: dict[str, int]
    explanation: str


class GroundingEngine:
    def __init__(self) -> None:
        self.log = ChronicleLog()

    def resolve(self, world: World, settlement_id: str, prompt: str) -> GroundedEffect:
        normalized = prompt.lower()
        settlement = world.settlements[settlement_id]
        if "spaceship" in normalized and world.logic.magic_tier != MagicTier.SCI_FI:
            effect = GroundedEffect(
                parsed_intent="Introduce advanced off-world technology.",
                plausibility="declined_world_breaking",
                materialized_effect={"type": "none"},
                first_consequence={},
                explanation="This world's logic cannot support off-world technology.",
            )
        elif "dragon" in normalized and world.logic.magic_tier == MagicTier.HIGH_MAGIC:
            effect = GroundedEffect(
                parsed_intent="Summon a dangerous winged predator.",
                plausibility="grounded_supernatural",
                materialized_effect={
                    "type": "entity",
                    "species": "dragon",
                    "behavior": "territorial predator",
                    "home_region": settlement.region_id,
                    "strength": 8,
                    "lifespan_days": 90,
                },
                first_consequence={"happiness": -8, "food": -10},
                explanation="A dragon appears as a real predator and immediately disrupts nearby herds.",
            )
        elif "dragon" in normalized:
            effect = GroundedEffect(
                parsed_intent="Summon a dragon.",
                plausibility="reinterpreted_low_magic",
                materialized_effect={
                    "type": "phenomenon",
                    "name": "mountain wildfire mistaken for a dragon",
                    "home_region": settlement.region_id,
                    "lifespan_days": 14,
                },
                first_consequence={"happiness": -5, "food": -4},
                explanation="The act resolves as smoke, fire, and fear inside the world's low-magic rules.",
            )
        elif "river" in normalized:
            effect = GroundedEffect(
                parsed_intent="Reveal an underground water source.",
                plausibility="grounded_environmental",
                materialized_effect={"type": "resource", "resource": "underground river"},
                first_consequence={"food": 12, "happiness": 4},
                explanation="A spring is discovered and irrigation improves immediately.",
            )
        else:
            effect = GroundedEffect(
                parsed_intent="Create a broad divine omen.",
                plausibility="minor_grounded_nudge",
                materialized_effect={"type": "omen", "name": "restless dreams"},
                first_consequence={"culture": 2},
                explanation="The settlement interprets the sign through local custom.",
            )
        self.log.append(
            world,
            kind=EventKind.DIVINE_ACT,
            actor="providence",
            text=prompt,
            payload={
                "settlement_id": settlement_id,
                "deltas": effect.first_consequence,
                "omen_log": effect.__dict__,
            },
        )
        return effect
