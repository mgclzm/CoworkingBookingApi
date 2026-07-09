from abc import abstractmethod

from domain.entities.refresh_token import RefreshToken
from infra.repositories.base_repository import BaseRepository

class BaseRefreshTokenRepository(BaseRepository[RefreshToken]):
    @abstractmethod
    async def find_all_by_user_id(self, user_id: str) -> list[RefreshToken]:
        ...