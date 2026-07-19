from dataclasses import dataclass, field
from uuid import uuid4
from domain.entities.base import BaseEntity, InactiveEntityUsageError, LogicException
from domain.entities.user import AppUser
from domain.values.workspace import Number, Title, WorkingTime, WorkspaceDescription, WorkspaceLocation

@dataclass    
class WorkplaceAlreadyExistError(LogicException):
    workplace: Workplace

    @property
    def message(self) -> str:
        return f'Workplace with number {self.workplace.number.value} already exist'

@dataclass(eq=False)
class Workplace(BaseEntity): 
    workplace_id: str = field(default_factory=lambda: str(uuid4()), kw_only=True)
    title: Title
    number: Number
    is_active: bool = field(default=True)

    def __eq__(self, other: Workplace) -> bool:
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

    def register_workplace(self, workplace: Workplace) -> None:
        if not workplace.is_active:
            raise InactiveEntityUsageError(self)
        if any(w.number == workplace.number for w in self._workplaces):
            raise WorkplaceAlreadyExistError(workplace)
        self._workplaces.add(workplace)

    