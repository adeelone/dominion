from backend.app.providence.blessings_curses import BlessingCurseService, MAX_MAGNITUDE
from backend.app.worldmind.client import WorldMind
from backend.app.simulation.archive_engine import ArchiveEngine
from backend.app.simulation.chronicle_log import ChronicleLog
from backend.app.simulation.clock import Clock
from backend.app.simulation.models import EventKind
from backend.app.simulation.rewind import RewindService
from backend.app.simulation.state_projection import StateProjection
from backend.app.worldgen.presets import demo_world


def test_region_tags_do_not_enter_prompt_context() -> None:
    world = demo_world()
    context = ChronicleLog().prompt_context(world)
    assert "floodplain" not in str(context)
    assert "drought-prone" in str(context)


def test_archive_engine_preserves_raw_ids_in_summary_payload() -> None:
    world = demo_world()
    log = ChronicleLog()
    for i in range(12):
        log.append(world, kind=EventKind.WORLD_EVENT, actor="test", text=f"event {i}")
    result = ArchiveEngine(threshold=12).maybe_compress(world)
    assert result.compressed_count == 12
    assert world.chronicle[-1].kind == EventKind.ARCHIVE_SUMMARY
    assert len(world.chronicle[-1].payload["raw_event_ids"]) == 12


def test_clock_advance_adds_days() -> None:
    world = demo_world()
    result = Clock().advance(world, "week")
    assert result.old_tick == 0
    assert result.new_tick == 7


def test_rewind_forks_without_overwriting_original() -> None:
    world = demo_world()
    log = ChronicleLog()
    first = log.append(world, kind=EventKind.WORLD_EVENT, actor="test", text="one")
    log.append(world, kind=EventKind.WORLD_EVENT, actor="test", text="two")
    fork = RewindService().fork_at_event(world, first.id)
    assert fork.branch_of == world.id
    assert len(fork.chronicle) == 1
    assert len(world.chronicle) == 2


def test_blessing_magnitude_is_bounded() -> None:
    world = demo_world()
    BlessingCurseService().apply(world, "s1", "fertility", 99, True)
    projected = StateProjection().project(world)
    assert projected.settlements["s1"].food == world.settlements["s1"].food + MAX_MAGNITUDE


def test_worldmind_records_token_and_credit_accounting() -> None:
    worldmind = WorldMind()
    response = worldmind.complete("archive", "compress these events", tier="deep")
    assert response.cost_credits == 5
    assert worldmind.calls[0].tokens_in == 3
    assert worldmind.calls[0].purpose == "archive"
