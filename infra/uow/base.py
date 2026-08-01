from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from types import TracebackType

from infra.repositories.booking.base import BaseBookingRepository
from infra.repositories.refresh_token.base import BaseRefreshTokenRepository
from infra.repositories.user.base import BaseUserRepository
from infra.repositories.workspace.base import BaseWorkspaceRepository


@dataclass
class BaseUnitOfWork(ABC):
    user_repository: BaseUserRepository = field(init=False)
    workspace_repository: BaseWorkspaceRepository = field(init=False)
    booking_repository: BaseBookingRepository = field(init=False)
    refresh_token_repository: BaseRefreshTokenRepository = field(init=False)

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ): ...

    @abstractmethod
    async def commit(self): ...
