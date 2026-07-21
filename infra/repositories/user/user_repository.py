from dataclasses import dataclass

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.user import AppUser
from domain.values.user import Email, Name, Password
from infra.repositories.user.user_model import AppUserModel

from .base import BaseUserRepository


def _convert_user_model_to_entity(user_model: AppUserModel) -> AppUser:
    name = Name(user_model.firstname, user_model.lastname)
    email = Email(user_model.email)
    password = Password(user_model.password)
    return AppUser(
        name,
        email,
        password,
        user_model.is_active,
        user_id=user_model.user_id,
        creation_time=user_model.creation_time,
    )


def _convert_user_entity_to_model(user: AppUser) -> AppUserModel:
    user_id = user.user_id
    firstname = user.name.first_name
    lastname = user.name.last_name
    email = user.email.value
    password = user.password.value
    creation_time = user.creation_time
    is_active = user.is_active
    return AppUserModel(
        user_id=user_id,
        firstname=firstname,
        lastname=lastname,
        email=email,
        password=password,
        creation_time=creation_time,
        is_active=is_active,
    )


@dataclass
class SqlAlchemyUserRepository(BaseUserRepository):
    _session: AsyncSession

    async def save(self, entity: AppUser) -> None:
        user_model = _convert_user_entity_to_model(entity)
        self._session.add(user_model)

    async def delete(self, entity: AppUser) -> None:
        user_model = _convert_user_entity_to_model(entity)
        await self._session.delete(user_model)

    async def merge(self, entity: AppUser) -> None:
        user_model = _convert_user_entity_to_model(entity)
        await self._session.merge(user_model)

    async def find_by_user_id(self, user_id: str) -> AppUser | None:
        result = await self._session.execute(
            select(AppUserModel).where(AppUserModel.user_id == user_id)
        )
        result = result.scalar_one_or_none()
        if not result:
            return None
        return _convert_user_model_to_entity(result)

    async def find_all_by_name(self, name: Name) -> list[AppUser]:
        firstname = name.first_name
        lastname = name.last_name
        result = await self._session.execute(
            select(AppUserModel).where(
                and_(
                    AppUserModel.firstname == firstname,
                    AppUserModel.lastname == lastname,
                )
            )
        )
        result = result.scalars().all()
        return [_convert_user_model_to_entity(user) for user in result]

    async def find_by_email(self, email: str) -> AppUser | None:
        result = await self._session.execute(
            select(AppUserModel).where(AppUserModel.email == email)
        )
        result = result.scalar_one_or_none()
        if not result:
            return None
        return _convert_user_model_to_entity(result)
