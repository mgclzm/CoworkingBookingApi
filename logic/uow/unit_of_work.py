from dataclasses import dataclass, field
from types import TracebackType
from typing import Type

from logic.uow.base import BaseUnitOfWork
from infra.repositories.booking.base import BaseBookingRepository
from infra.repositories.booking.booking_repository import SqlAlchemyBookingRepository
from infra.repositories.user.base import BaseUserRepository
from infra.repositories.user.user_repository import SqlAlchemyUserRepository
from infra.repositories.workspace.base import BaseWorkspaceRepository
from infra.repositories.workspace.workspace_repository import SqlAlchemyWorkspaceRepository

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

DEFAULT_SESSION_FACTORY = async_sessionmaker(bind=create_async_engine('settings.postgres_url()'), 
                                             autoflush=False, expire_on_commit=False)

@dataclass
class SqlAlchemyUnitOfWork(BaseUnitOfWork):
    _session_factory: async_sessionmaker[AsyncSession] = field(default=DEFAULT_SESSION_FACTORY)
    _session: AsyncSession = field(init=False)
    user_repository: BaseUserRepository = field(init=False)
    workspace_repository: BaseWorkspaceRepository = field(init=False)
    booking_repository: BaseBookingRepository = field(init=False)
    
    async def __aenter__(self) -> SqlAlchemyUnitOfWork:
        self._session = self._session_factory() 
        self.user_repository = SqlAlchemyUserRepository(self._session)
        self.workspace_repository = SqlAlchemyWorkspaceRepository(self._session)
        self.booking_repository = SqlAlchemyBookingRepository(self._session)
        return self
    
    async def __aexit__(self, exc_type: Type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None) -> None:
        try:
            if exc_type:
                await self._session.rollback()
        finally:
            await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()
    
    async def _rollback(self):
        await self._session.rollback()
            