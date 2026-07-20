from dataclasses import dataclass
from datetime import time

from api.routes.workspace.schemas import AddWorkplaceResponseSchema, RegisterWorkspaceResponseSchema
from logic.commands.base import BaseCommand

@dataclass(frozen=True)
class RegisterWorkspaceCommand(BaseCommand[RegisterWorkspaceResponseSchema]):
    owner_id: str
    opening_time: time
    closing_time: time
    location: str
    description: str

@dataclass(frozen=True)
class AddWorkplaceCommand(BaseCommand[AddWorkplaceResponseSchema]):
    user_id: str
    workspace_id: str
    title: str
    number: int
