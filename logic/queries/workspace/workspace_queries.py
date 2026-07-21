from dataclasses import dataclass, field

from api.routes.workspace.schemas import GetAllWorkspacesResponseSchema
from logic.queries.base import BaseQuery

@dataclass(frozen=True)
class GetAllWorkspacesQuery(BaseQuery[list[GetAllWorkspacesResponseSchema]]):
    page_number: int
    page_size: int
    city: str | None
