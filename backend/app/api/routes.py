from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.app.api.schemas import AdvanceRequest, CommandRequest
from backend.app.providence.blessings_curses import BlessingCurseService
from backend.app.providence.disasters import DisasterService
from backend.app.providence.grounding_engine import GroundingEngine
from backend.app.simulation.clock import Clock
from backend.app.simulation.state_projection import StateProjection
from backend.app.throne.chancellor import Chancellor
from backend.app.throne.decrees import DecreeService
from backend.app.worldgen.presets import demo_world

router = APIRouter()
world = demo_world()


@router.get("/worlds/demo")
def get_world() -> dict[str, object]:
    projected = StateProjection().project(world)
    return {"world": projected, "chancellor": Chancellor().brief(projected)}


@router.post("/worlds/demo/throne/decrees")
def issue_decree(request: CommandRequest) -> dict[str, object]:
    result = DecreeService().issue(world, request.target_id, request.text)
    if not result.accepted:
        raise HTTPException(status_code=422, detail=result.explanation)
    return {"result": result, "world": StateProjection().project(world)}


@router.post("/worlds/demo/providence/acts")
def divine_act(request: CommandRequest) -> dict[str, object]:
    effect = GroundingEngine().resolve(world, request.target_id, request.text)
    return {"effect": effect, "world": StateProjection().project(world)}


@router.post("/worlds/demo/providence/blessings")
def blessing(request: CommandRequest) -> dict[str, object]:
    BlessingCurseService().apply(world, request.target_id, request.text, 8, True)
    return {"world": StateProjection().project(world)}


@router.post("/worlds/demo/providence/disasters")
def disaster(request: CommandRequest) -> dict[str, object]:
    DisasterService().invoke(world, request.target_id, request.text)
    return {"world": StateProjection().project(world)}


@router.post("/worlds/demo/advance")
def advance(request: AdvanceRequest) -> dict[str, object]:
    return {"clock": Clock().advance(world, request.amount), "world": StateProjection().project(world)}
