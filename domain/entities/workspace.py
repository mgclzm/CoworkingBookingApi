from dataclasses import dataclass, field
from uuid import uuid4
from domain.exceptions.errors import InactiveEntityUsageError
from domain.values.booking import BookingTime
from domain.values.workspace import SpotNumber, SpotTitle, WorkingTime, WorkspaceDescription

@dataclass(eq=False)
class Workplace: 
    workplace_id: str = field(default_factory=lambda: str(uuid4()))
    title: SpotTitle = field(kw_only=True)
    number: SpotNumber = field(kw_only=True)
    is_active: bool = field(default=True)

    def __eq__(self, other: Workplace) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.workplace_id == other.workplace_id
    
    def __hash__(self) -> int:
        return hash(self.workplace_id)

@dataclass
class Workspace:
    workspace_id: str = field(default_factory=lambda: str(uuid4()))
    workplaces: set[Workplace] = field(default_factory=set)
    working_time: WorkingTime = field(kw_only=True)
    description: WorkspaceDescription = field(kw_only=True)
    is_active: bool = field(default=True)

    def register_workplace(self, workplace: Workplace) -> None:
        if not workplace.is_active:
            raise InactiveEntityUsageError('Workplace is not active')
        self.workplaces.add(workplace)

    