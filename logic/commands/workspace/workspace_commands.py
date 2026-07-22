from dataclasses import dataclass
from datetime import time

from api.routes.workspace.schemas import (
    AddWorkplaceResponseSchema,
    RegisterWorkspaceResponseSchema,
)
from logic.commands.base import BaseCommand


@dataclass(frozen=True)
class RegisterWorkspaceCommand(BaseCommand[RegisterWorkspaceResponseSchema]):
    owner_id: str
    opening_time: time
    closing_time: time
    city: str
    street: str
    description: str


@dataclass(frozen=True)
class AddWorkplaceCommand(BaseCommand[AddWorkplaceResponseSchema]):
    user_id: str
    workspace_id: str
    title: str
    number: int


@dataclass(frozen=True)
class PatchWorkspaceCommand(BaseCommand[None]):
    workspace_id: str
    user_id: str
    city: str | None
    street: str | None
    opening_time: time | None
    closing_time: time | None
    description: str | None
