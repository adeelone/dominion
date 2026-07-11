from __future__ import annotations

from pydantic import BaseModel


class CommandRequest(BaseModel):
    text: str
    target_id: str


class AdvanceRequest(BaseModel):
    amount: int | str


class ReportRequest(BaseModel):
    world_id: str
    reason: str
