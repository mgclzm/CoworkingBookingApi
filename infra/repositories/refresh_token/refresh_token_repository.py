from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.refresh_token import RefreshToken
from infra.repositories.refresh_token.base import BaseRefreshTokenRepository
from infra.repositories.refresh_token.refresh_token_model import RefreshTokenModel

def _convert_refresh_token_entity_to_model(refresh_token_entity: RefreshToken) -> RefreshTokenModel:
    token_id = refresh_token_entity.token_id
    user_id = refresh_token_entity.user_id
    expires_at = refresh_token_entity.expires_at
    revoked = refresh_token_entity.revoked
    created_at = refresh_token_entity.created_at
    return RefreshTokenModel(token_id=token_id, user_id=user_id, expires_at=expires_at,
                             revoked=revoked, created_at=created_at)

def _convert_refresh_token_model_to_entity(refresh_token_model: RefreshTokenModel) -> RefreshToken:
    token_id = refresh_token_model.token_id
    user_id = refresh_token_model.user_id
    expires_at = refresh_token_model.expires_at
    revoked = refresh_token_model.revoked
    created_at = refresh_token_model.created_at
    return RefreshToken(user_id, expires_at, revoked, token_id=token_id, created_at=created_at)

@dataclass
class SqlAlchemyRefreshTokenRepository(BaseRefreshTokenRepository):
    _session: AsyncSession

    async def save(self, entity: RefreshToken) -> None:
        refresh_token_model = _convert_refresh_token_entity_to_model(entity)
        self._session.add(refresh_token_model)
    
    async def delete(self, entity: RefreshToken) -> None:
        refresh_token_model = _convert_refresh_token_entity_to_model(entity)
        await self._session.delete(refresh_token_model)

    async def merge(self, entity: RefreshToken) -> None:
        refresh_token_model = _convert_refresh_token_entity_to_model(entity)
        await self._session.merge(refresh_token_model)

    async def find_all_by_user_id(self, user_id: str) -> list[RefreshToken]:
        result = await self._session.execute(select(RefreshTokenModel).where(RefreshTokenModel.user_id == user_id))
        result = result.scalars().all()
        return [_convert_refresh_token_model_to_entity(token) for token in result]
    
    async def find_by_token_id(self, token_id: str) -> RefreshToken | None:
        result = await self._session.execute(select(RefreshTokenModel).where(RefreshTokenModel.token_id == token_id))
        result = result.scalar_one_or_none()
        if result is None:
            return None
        return _convert_refresh_token_model_to_entity(result)
