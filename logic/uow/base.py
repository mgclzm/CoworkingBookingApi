from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from types import TracebackType
from typing import Type

from infra.repositories.booking.base import BaseBookingRepository
from infra.repositories.user.base import BaseUserRepository
from infra.repositories.workspace.base import BaseWorkspaceRepository

@dataclass
class BaseUnitOfWork(ABC):
    user_repository: BaseUserRepository = field(init=False)
    workspace_repository: BaseWorkspaceRepository = field(init=False)
    booking_repository: BaseBookingRepository = field(init=False)
    
    @abstractmethod
    async def __aenter__(self):
        ...
    
    @abstractmethod
    async def __aexit__(self, exc_type: Type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None):
        ...
    
    @abstractmethod
    async def commit(self):
        ...
    
    # @abstractmethod
    # async def _rollback(self):
    #     ...