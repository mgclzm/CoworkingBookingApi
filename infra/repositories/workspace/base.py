from abc import abstractmethod

from domain.entities.workspace import Workplace, Workspace
from domain.values.booking import BookingTime
from infra.repositories.base_repository import BaseRepository

class BaseWorkspaceRepository(BaseRepository[Workspace]):
    @abstractmethod
    async def find_all(self) -> list[Workspace]:
        ...
    
    @abstractmethod
    async def find_by_workspace_id(self, workspace_id: str) -> Workspace | None:
        ...
    
    @abstractmethod
    async def find_all_available_places(self, workspace_id: str, booking_time: BookingTime) -> list[Workplace]:
        ...
