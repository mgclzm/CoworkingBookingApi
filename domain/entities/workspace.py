from dataclasses import dataclass, field
from datetime import time
from typing import Iterator
from uuid import uuid4

from api.routes.user.security import AuthException
from domain.entities.base import BaseEntity, InactiveEntityUsageError, LogicException
from domain.values.workspace import (
    Number,
    Title,
    WorkingTime,
    WorkspaceDescription,
    WorkspaceLocation,
)


@dataclass
class WorkplaceAlreadyExistError(LogicException):
    workplace: "Workplace"

    @property
    def message(self) -> str:
        return f"Workplace with number {self.workplace.number.value} already exist"


@dataclass
class WorkspaceNotFoundError(LogicException):
    workspace_id: str

    @property
    def message(self) -> str:
        return f'Workspace with "{self.workspace_id}" id not found'


@dataclass
class WorkspaceAccessDeniedError(AuthException):
    @property
    def message(self) -> str:
        return "Access to workspace is denied"


@dataclass(eq=False)
class Workplace(BaseEntity):
    workplace_id: str = field(default_factory=lambda: str(uuid4()), kw_only=True)
    title: Title
    number: Number
    is_active: bool = field(default=True)

    def __eq__(self, other: "Workplace") -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.workplace_id == other.workplace_id

    def __hash__(self) -> int:
        return hash(self.workplace_id)


@dataclass
class Workspace(BaseEntity):
    workspace_id: str = field(default_factory=lambda: str(uuid4()), kw_only=True)
    _workplaces: set[Workplace] = field(default_factory=set, kw_only=True)
    location: WorkspaceLocation
    working_time: WorkingTime
    description: WorkspaceDescription
    owner_id: str
    is_active: bool = field(default=True)

    def __iter__(self) -> Iterator[Workplace]:
        return iter(self._workplaces)

    def register_workplace(self, workplace: Workplace) -> None:
        if not workplace.is_active:
            raise InactiveEntityUsageError(self)
        if any(w.number == workplace.number for w in self._workplaces):
            raise WorkplaceAlreadyExistError(workplace)
        self._workplaces.add(workplace)

    def ensure_owned_by(self, user_id: str) -> None:
        if self.owner_id != user_id:
            raise WorkspaceAccessDeniedError()

    def update_location(
        self, *, city: str | None = None, street: str | None = None
    ) -> None:
        if (city is None) and (street is None):
            return

        new_location = WorkspaceLocation(
            city=city if city is not None else self.location.city,
            street=street if street is not None else self.location.street,
        )

        self.location = new_location

    def update_working_time(
        self, *, opening_time: time | None = None, closing_time: time | None = None
    ) -> None:
        if (opening_time is None) and (closing_time is None):
            return

        new_working_time = WorkingTime(
            opening_time=opening_time
            if opening_time is not None
            else self.working_time.opening_time,
            closing_time=closing_time
            if closing_time is not None
            else self.working_time.closing_time,
        )

        self.working_time = new_working_time

    def update_description(self, description: str | None = None) -> None:
        if description is None:
            return

        new_description = WorkspaceDescription(description)
        self.description = new_description
