from dataclasses import dataclass

from api.routes.user.schemas import (
    IssueRefreshTokenResponseSchema,
    RegisterUserResponseSchema,
)
from logic.commands.base import BaseCommand


@dataclass(frozen=True)
class RegisterUserCommand(BaseCommand[RegisterUserResponseSchema]):
    first_name: str
    last_name: str
    email: str
    password: str


@dataclass(frozen=True)
class IssueRefreshTokenCommand(BaseCommand[IssueRefreshTokenResponseSchema]):
    email: str
    password: str


@dataclass(frozen=True)
class LogoutCommand(BaseCommand[None]):
    jti: str
