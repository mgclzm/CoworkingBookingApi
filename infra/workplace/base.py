from abc import abstractmethod

from domain.entities.workspace import Workplace, Workspace
from domain.values.booking import BookingTime
from infra.base_repository import BaseRepository

class BaseWorkplaceRepository(BaseRepository[Workplace]):
    @abstractmethod
    async def find_all_by_workspace(self, workspace_id: str) -> list[Workplace]:
        ...
    
    @abstractmethod
    async def find_all_available(self, workspace_id: str, bookind_time: BookingTime) -> list[Workplace]:
        ...
    
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
