from abc import abstractmethod

from domain.entities.user import AppUser
from domain.values.user import Name
from infra.repositories.base_repository import BaseRepository


class BaseUserRepository(BaseRepository[AppUser]):
    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> AppUser | None: ...

    @abstractmethod
    async def find_all_by_name(self, name: Name) -> list[AppUser]: ...

    @abstractmethod
    async def find_by_email(self, email: str) -> AppUser | None: ...
