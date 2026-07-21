from datetime import time

from pydantic import BaseModel, Field

from domain.entities.workspace import Workplace, Workspace


class RegisterWorkspaceRequestSchema(BaseModel):
    opening_time: time
    closing_time: time
    city: str
    street: str
    description: str


class RegisterWorkspaceResponseSchema(BaseModel):
    workspace_id: str


class AddWorkplaceRequestSchema(BaseModel):
    title: str
    number: int


class AddWorkplaceResponseSchema(BaseModel):
    workplace_id: str
    title: str
    number: int


class GetWorkplacesParams(BaseModel):
    page_number: int = Field(default=1, gt=0)
    page_size: int = Field(default=10, gt=0, le=30)
    city: str | None = Field(default=None, max_length=50)


class WorkplaceSchema(BaseModel):
    workplace_id: str
    title: str
    number: int
    is_active: bool

    @staticmethod
    def from_entity(entity: Workplace) -> "WorkplaceSchema":
        return WorkplaceSchema(
            workplace_id=entity.workplace_id,
            title=entity.title.value,
            number=entity.number.value,
            is_active=entity.is_active,
        )


class WorkspaceSchema(BaseModel):
    workspace_id: str
    city: str
    street: str
    opening_time: time
    closing_time: time
    description: str
    is_active: bool
    workplaces: list[WorkplaceSchema]

    @staticmethod
    def from_entity(entity: Workspace) -> "WorkspaceSchema":
        workplaces = [WorkplaceSchema.from_entity(workplace) for workplace in entity]
        return WorkspaceSchema(
            workspace_id=entity.workspace_id,
            city=entity.location.city,
            street=entity.location.street,
            opening_time=entity.working_time.opening_time,
            closing_time=entity.working_time.closing_time,
            description=entity.description.value,
            is_active=entity.is_active,
            workplaces=workplaces,
        )
