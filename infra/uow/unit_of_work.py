from dataclasses import dataclass, field
from types import TracebackType
from typing import Self

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from infra.repositories.booking.booking_repository import SqlAlchemyBookingRepository
from infra.repositories.refresh_token.refresh_token_repository import (
    SqlAlchemyRefreshTokenRepository,
)
from infra.repositories.user.user_repository import SqlAlchemyUserRepository
from infra.repositories.workspace.workspace_repository import (
    SqlAlchemyWorkspaceRepository,
)
from infra.settings.settings import settings
from infra.uow.base import BaseUnitOfWork

DEFAULT_SESSION_FACTORY = async_sessionmaker(
    bind=create_async_engine(settings.postgres_db_url),
    autoflush=False,
    expire_on_commit=False,
)


@dataclass
class SqlAlchemyUnitOfWork(BaseUnitOfWork):
    cache: Redis
    _session_factory: async_sessionmaker[AsyncSession] = field(
        default=DEFAULT_SESSION_FACTORY
    )
    _session: AsyncSession = field(init=False)

    async def __aenter__(self) -> Self:
        self._session = self._session_factory()
        self.user_repository = SqlAlchemyUserRepository(self._session)
        self.workspace_repository = SqlAlchemyWorkspaceRepository(self._session)
        self.booking_repository = SqlAlchemyBookingRepository(self._session)
        self.refresh_token_repository = SqlAlchemyRefreshTokenRepository(self._session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        try:
            if exc_type:
                await self._session.rollback()
        finally:
            await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()
