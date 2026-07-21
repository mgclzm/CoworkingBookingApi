from dataclasses import dataclass

from api.routes.user.schemas import (
    AccessTokenResponseSchema,
    GetCurrentUserResponseSchema,
)
from logic.queries.base import BaseQuery


@dataclass(frozen=True)
class AccessTokenQuery(BaseQuery[AccessTokenResponseSchema]):
    user_id: str


@dataclass(frozen=True)
class GetCurrentUserQuery(BaseQuery[GetCurrentUserResponseSchema]):
    user_id: str
