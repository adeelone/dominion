from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.app.api.schemas import AdvanceRequest, CommandRequest, ReportRequest
from backend.app.moderation.policy import ModerationPolicy
from backend.app.providence.blessings_curses import BlessingCurseService
from backend.app.providence.disasters import DisasterService
from backend.app.providence.grounding_engine import GroundingEngine
from backend.app.simulation.models import EventKind
from backend.app.simulation.clock import Clock
from backend.app.simulation.chronicle_log import ChronicleLog
from backend.app.simulation.state_projection import StateProjection
from backend.app.throne.chancellor import Chancellor
from backend.app.throne.decrees import DecreeService
from backend.app.worldgen.presets import demo_world
from backend.app.worldmind.client import WorldMind

router = APIRouter()
world = demo_world()
moderation = ModerationPolicy()
worldmind = WorldMind()
reports: list[dict[str, object]] = []


def require_allowed(text: str) -> None:
    allowed, reason = moderation.check(text)
    if not allowed:
        raise HTTPException(status_code=400, detail=reason)


@router.get("/worlds/demo")
def get_world() -> dict[str, object]:
    projected = StateProjection().project(world)
    return {"world": projected, "chancellor": Chancellor().brief(projected), "worldmind_calls": worldmind.calls}


@router.post("/worlds/demo/throne/decrees")
def issue_decree(request: CommandRequest) -> dict[str, object]:
    require_allowed(request.text)
    worldmind.complete("decree_interpretation", request.text, tier="fast")
    result = DecreeService().issue(world, request.target_id, request.text)
    if not result.accepted:
        raise HTTPException(status_code=422, detail=result.explanation)
    return {"result": result, "world": StateProjection().project(world)}


@router.post("/worlds/demo/providence/acts")
def divine_act(request: CommandRequest) -> dict[str, object]:
    require_allowed(request.text)
    worldmind.complete("divine_act_grounding", request.text, tier="deep")
    effect = GroundingEngine().resolve(world, request.target_id, request.text)
    return {"effect": effect, "world": StateProjection().project(world)}


@router.post("/worlds/demo/providence/blessings")
def blessing(request: CommandRequest) -> dict[str, object]:
    require_allowed(request.text)
    BlessingCurseService().apply(world, request.target_id, request.text, 8, True)
    return {"world": StateProjection().project(world)}


@router.post("/worlds/demo/providence/disasters")
def disaster(request: CommandRequest) -> dict[str, object]:
    require_allowed(request.text)
    DisasterService().invoke(world, request.target_id, request.text)
    return {"world": StateProjection().project(world)}


@router.post("/worlds/demo/advance")
def advance(request: AdvanceRequest) -> dict[str, object]:
    return {"clock": Clock().advance(world, request.amount), "world": StateProjection().project(world)}


@router.get("/worlds/demo/export")
def export_world() -> dict[str, object]:
    projected = StateProjection().project(world)
    return {
        "world_id": projected.id,
        "name": projected.name,
        "tick": projected.tick,
        "logic": projected.logic,
        "regions": projected.regions,
        "polities": projected.polities,
        "settlements": projected.settlements,
        "chronicle": projected.chronicle,
    }


@router.post("/reports")
def report_world(request: ReportRequest) -> dict[str, object]:
    require_allowed(request.reason)
    report: dict[str, object] = {
        "world_id": request.world_id,
        "reason": request.reason,
        "status": "queued",
    }
    reports.append(report)
    ChronicleLog().append(
        world,
        kind=EventKind.WORLD_EVENT,
        actor="moderation",
        text="A world report entered the review queue.",
        payload=report,
    )
    return report
