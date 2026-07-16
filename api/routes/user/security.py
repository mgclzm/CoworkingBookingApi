from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, NamedTuple, cast

import jwt

from datetime import datetime, timedelta, timezone
from enum import StrEnum

from domain.entities.refresh_token import RefreshToken
from infra.settings.settings import settings
from logic.uow.base import BaseUnitOfWork

class TokenType(StrEnum):
    REFRESH = 'REFRESH'
    ACCESS = 'ACCESS'

def encode_refresh_token(refresh_token: RefreshToken) -> str:
    secret = settings.refresh_token_secret
    algorithm = settings.token_algorithm
    payload = {
        'sub': refresh_token.user_id,
        'jti': refresh_token.token_id,
        'iat': refresh_token.created_at,
        'exp': refresh_token.expires_at,
        'type': TokenType.REFRESH
    }
    encoded_refresh_token = jwt.encode(payload, key=secret, algorithm=algorithm)
    return encoded_refresh_token

class RefreshTokenData(NamedTuple):
    sub: str
    jti: str

def encode_access_token(sub: str) -> str:
    algorithm = settings.token_algorithm
    secret = settings.access_token_secret
    expiration = datetime.now(timezone.utc) + timedelta(seconds=settings.access_token_lifetime)
    payload = {
        'sub': sub,
        'exp': expiration,
        'type': TokenType.ACCESS
    }
    encoded_access_token = jwt.encode(payload, secret, algorithm)
    return encoded_access_token

@dataclass
class AuthException(ABC, BaseException):
    @property
    @abstractmethod
    def message(self) -> str:
        ...

@dataclass
class WrongTokenTypeError(AuthException):
    expected_type: str

    @property
    def message(self) -> str:
        return f'Token type is not "{self.expected_type}"'

@dataclass
class MissingClaimError(AuthException):
    missing_claim: str

    @property
    def message(self) -> str:
        return f'Token missing "{self.missing_claim}" claim'

@dataclass
class RefreshTokenNotFoundError(AuthException):
    jti: str

    @property
    def message(self) -> str:
        return f'Token with "{self.jti}" id not found'

@dataclass
class InvalidTokenIdError(AuthException):
    @property
    def message(self) -> str:
        return 'Token id mismatch'

@dataclass
class TokenRevokedError(AuthException):
    @property
    def message(self) -> str:
        return 'Token has been revoked'

class IRefreshTokenValidator(ABC):
    @abstractmethod
    async def validate(self, refresh_token_payload: dict[str, Any]) -> None:
        ...

@dataclass(frozen=True, slots=True)
class CompositeRefreshTokenValidator(IRefreshTokenValidator):
    required_claims_validator: IRefreshTokenValidator # doubtful
    validators: list[IRefreshTokenValidator]
    async def validate(self, refresh_token_payload: dict[str, Any]) -> None:
        await self.required_claims_validator.validate(refresh_token_payload)
        for validator in self.validators:
            await validator.validate(refresh_token_payload)

@dataclass(frozen=True, slots=True)
class RefreshTokenClaimsValidator(IRefreshTokenValidator):
    async def validate(self, refresh_token_payload: dict[str, Any]):
        if refresh_token_payload.get('sub') is None:
            raise MissingClaimError('sub')
        
        if refresh_token_payload.get('jti') is None:
            raise MissingClaimError('jti')
        
        if refresh_token_payload.get('iat') is None:
            raise MissingClaimError('iat')
        
        if refresh_token_payload.get('exp') is None:
            raise MissingClaimError('exp')
        
        if refresh_token_payload.get('type') is None:
            raise MissingClaimError('type')

@dataclass(frozen=True, slots=True)
class RefreshTokenTypeValidator(IRefreshTokenValidator):
    async def validate(self, refresh_token_payload: dict[str, Any]) -> None:
        token_type = cast(TokenType, refresh_token_payload.get('type'))
        if token_type != TokenType.REFRESH:
            raise WrongTokenTypeError(expected_type=TokenType.REFRESH)

@dataclass(frozen=True, slots=True)
class RefreshTokenJtiValidator(IRefreshTokenValidator):
    uow: BaseUnitOfWork
    async def validate(self, refresh_token_payload: dict[str, Any]) -> None:
        async with self.uow:
            user_id = cast(str, refresh_token_payload.get('sub'))
            found_refresh_tokens = await self.uow.refresh_token_repository.find_all_by_user_id(user_id)
            if not found_refresh_tokens:
                raise RefreshTokenNotFoundError('User dont have any refresh tokens')
            
            jti = cast(str, refresh_token_payload.get('jti'))
            matching_token = next(
                (token for token in found_refresh_tokens if token.token_id == jti),
                None
            )

            if matching_token is None:
                raise InvalidTokenIdError()
            if matching_token.revoked:
                raise TokenRevokedError()
