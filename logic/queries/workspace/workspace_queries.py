from dataclasses import dataclass

from api.routes.workspace.schemas import WorkspaceSchema
from logic.queries.base import BaseQuery


@dataclass(frozen=True)
class GetAllWorkspacesQuery(BaseQuery[list[WorkspaceSchema]]):
    page_number: int
    page_size: int
    city: str | None


@dataclass(frozen=True)
class GetMyWorkspacesQuery(BaseQuery[list[WorkspaceSchema]]):
    user_id: str
    page_number: int
    page_size: int
