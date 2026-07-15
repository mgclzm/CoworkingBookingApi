from dataclasses import dataclass, field
from datetime import time
from uuid import uuid4
from domain.entities.base import ApplicationException, BaseEntity, InactiveEntityUsageError, LogicException
from domain.values.workspace import Number, Title, WorkingTime, WorkspaceDescription

@dataclass
class InvalidTitleError(ApplicationException):
    title_value: str

    @property
    def message(self) -> str:
        return f'Title value cannot be empty or bigger then 50 characters, got {self.title_value}'

@dataclass
class InvalidNumberError(ApplicationException):
    number_value: int

    @property
    def message(self) -> str:
        return f'Spot number must be between 1 and 100, got {self.number_value}'

@dataclass
class InvalidWorkingTimeError(ApplicationException):
    opening_time: time
    closing_time: time

    @property
    def message(self) -> str:
        return f'Opening time must be before closing time, got opening time = {self.opening_time}, closing time = {self.closing_time}'

@dataclass
class InvalidDescriptionError(ApplicationException):
    description_value: str

    @property
    def message(self) -> str:
        return f'Workspace description must me less then 1000, actual length {len(self.description_value)}'

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
    working_time: WorkingTime 
    description: WorkspaceDescription
    is_active: bool = field(default=True)

    def register_workplace(self, workplace: Workplace) -> None:
        if not workplace.is_active:
            raise InactiveEntityUsageError(self)
        if any(w.number == workplace.number for w in self._workplaces):
            raise WorkplaceAlreadyExistError(workplace)
        self._workplaces.add(workplace)

    