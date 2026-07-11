from __future__ import annotations

from backend.app.simulation.models import MagicTier, Polity, Region, Settlement, World, WorldLogic


def demo_world() -> World:
    regions = {
        "r1": Region("r1", "Crown Basin", "riverland", ("grain", "floodplain"), ((0, 0), (42, 8), (34, 42))),
        "r2": Region("r2", "Ashen March", "mountain", ("iron", "storms"), ((46, 4), (90, 16), (64, 58))),
        "r3": Region("r3", "Southmere", "coast", ("fish", "trade"), ((10, 48), (54, 56), (20, 88))),
    }
    return World(
        id="world-demo",
        name="The Crown Basin",
        logic=WorldLogic(
            magic_tier=MagicTier.HIGH_MAGIC,
            tech_era="late bronze",
            briefing="A river kingdom, mountain clans, and coastal traders compete under unstable omens.",
            allowed_entities=("dragon", "prophet", "spirit", "giant stag"),
        ),
        regions=regions,
        polities={
            "p1": Polity("p1", "House Veyr", ("r1",), ("agrarian", "centralized")),
            "p2": Polity("p2", "March Clans", ("r2",), ("fractious", "iron-rich")),
        },
        settlements={
            "s1": Settlement("s1", "Bellroot", "r1", 420, 62, 130, 20, ("drought-prone",)),
            "s2": Settlement("s2", "Emberwatch", "r2", 210, 51, 70, 15, ("hardy", "superstitious")),
            "s3": Settlement("s3", "Marrow Quay", "r3", 300, 66, 110, 24, ("seafaring",)),
        },
    )


HISTORICAL_BASEMAPS = ["Bronze Coast 1200 BCE", "Silk Road Fractures 800 CE", "River Republics 1500 CE"]
INVENTED_PRESETS = ["Crown Basin High Magic", "Orbital Marches Sci-Fi Frontier"]
