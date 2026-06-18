from dataclasses import dataclass, field
from uuid import uuid4
from domain.exceptions.errors import InactiveEntityUsageError, WorkplaceAlreadyExistError
from domain.values.workspace import Number, Title, WorkingTime, WorkspaceDescription

@dataclass(eq=False)
class Workplace: 
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
class Workspace:
    workspace_id: str = field(default_factory=lambda: str(uuid4()), kw_only=True)
    _workplaces: set[Workplace] = field(default_factory=set, kw_only=True)
    working_time: WorkingTime 
    description: WorkspaceDescription
    is_active: bool = field(default=True)

    def register_workplace(self, workplace: Workplace) -> None:
        if not workplace.is_active:
            raise InactiveEntityUsageError('Workplace is not active')
        if any(w.number == workplace.number for w in self._workplaces):
            raise WorkplaceAlreadyExistError(f'Workplace with "{workplace.number}" already exist')
        self._workplaces.add(workplace)

    