from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError

from api.routes.user.schemas import (
    AccessTokenResponseSchema,
    GetCurrentUserResponseSchema,
    IssueRefreshTokenResponseSchema,
    RegisterUserResponseSchema,
)
from api.routes.user.security import (
    RefreshTokenNotFoundError,
    TokenType,
    encode_access_token,
    encode_refresh_token,
)
from domain.entities.refresh_token import RefreshToken
from domain.entities.user import (
    AppUser,
    EmailAlreadyExistError,
    InvalidUserCredentialsError,
    UserNotFoundError,
)
from domain.values.user import Email, Name, Password
from infra.settings.settings import settings
from logic.commands.user.user_commands import (
    IssueRefreshTokenCommand,
    LogoutCommand,
    RegisterUserCommand,
)
from logic.handlers.base import CommandHandler, QueryHandler
from logic.queries.user.user_queries import AccessTokenQuery, GetCurrentUserQuery
from logic.uow.base import BaseUnitOfWork


@dataclass
class RegisterUserCommandHandler(
    CommandHandler[RegisterUserCommand, RegisterUserResponseSchema]
):
    _uow: BaseUnitOfWork

    async def handle(self, command: RegisterUserCommand) -> RegisterUserResponseSchema:
        async with self._uow:
            if await self._uow.user_repository.find_by_email(command.email):
                raise EmailAlreadyExistError(command.email)

            user_name = Name(command.first_name, command.last_name)
            email = Email(command.email)
            ph = PasswordHasher()
            password = Password(ph.hash(command.password))
            new_user = AppUser(user_name, email, password)

            await self._uow.user_repository.save(new_user)
            await self._uow.commit()

            response_schema = RegisterUserResponseSchema(
                first_name=new_user.name.first_name,
                last_name=new_user.name.last_name,
                email=new_user.email.value,
                user_id=new_user.user_id,
                created_at=new_user.creation_time,
            )
            return response_schema


@dataclass
class IssueRefreshTokenCommandHandler(
    CommandHandler[IssueRefreshTokenCommand, IssueRefreshTokenResponseSchema]
):
    _uow: BaseUnitOfWork

    async def handle(
        self, query: IssueRefreshTokenCommand
    ) -> IssueRefreshTokenResponseSchema:
        async with self._uow:
            found_user = await self._uow.user_repository.find_by_email(query.email)
            if not found_user:
                raise UserNotFoundError(email=query.email)
            ph = PasswordHasher()
            try:
                ph.verify(found_user.password.value, query.password)
            except VerificationError:
                raise InvalidUserCredentialsError()

            sub = found_user.user_id
            exp = datetime.now(tz=timezone.utc) + timedelta(
                seconds=settings.refresh_token_lifetime
            )
            refresh_token = RefreshToken(sub, exp)
            encoded_refresh_token = encode_refresh_token(refresh_token)
            encoded_access_token = encode_access_token(sub)

            await self._uow.refresh_token_repository.save(refresh_token)
            await self._uow.commit()

            response_schema = IssueRefreshTokenResponseSchema(
                refresh_token=encoded_refresh_token, access_token=encoded_access_token
            )
            return response_schema


@dataclass
class AccessTokenQueryHandler(
    QueryHandler[AccessTokenQuery, AccessTokenResponseSchema]
):
    async def handle(self, query: AccessTokenQuery) -> AccessTokenResponseSchema:
        sub = query.user_id
        encoded_access_token = encode_access_token(sub)
        response_schema = AccessTokenResponseSchema(
            token_type=TokenType.ACCESS, access_token=encoded_access_token
        )
        return response_schema


@dataclass
class GetCurrentUserQueryHandler(
    QueryHandler[GetCurrentUserQuery, GetCurrentUserResponseSchema]
):
    _uow: BaseUnitOfWork

    async def handle(self, query: GetCurrentUserQuery) -> GetCurrentUserResponseSchema:
        async with self._uow:
            found_user = await self._uow.user_repository.find_by_user_id(query.user_id)
            if found_user is None:
                raise UserNotFoundError(user_id=query.user_id)
            user_id = found_user.user_id
            first_name = found_user.name.first_name
            last_name = found_user.name.last_name
            email = found_user.email.value
            response_schema = GetCurrentUserResponseSchema(
                user_id=user_id, first_name=first_name, last_name=last_name, email=email
            )
            return response_schema


@dataclass
class LogoutCommandHandler(CommandHandler[LogoutCommand, None]):
    _uow: BaseUnitOfWork

    async def handle(self, command: LogoutCommand) -> None:
        async with self._uow:
            found_token = await self._uow.refresh_token_repository.find_by_token_id(
                command.jti
            )
            if found_token is None:
                raise RefreshTokenNotFoundError(command.jti)

            found_token.revoke()

            await self._uow.refresh_token_repository.merge(found_token)
            await self._uow.commit()
