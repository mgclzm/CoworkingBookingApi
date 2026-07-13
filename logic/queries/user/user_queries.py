from dataclasses import dataclass

from api.routes.user.schemas import AccessTokenResponseSchema, GetCurrentUserResponseSchema, RefreshTokenResponseSchema
from logic.queries.base import BaseQuery

@dataclass
class RefreshTokenQuery(BaseQuery[RefreshTokenResponseSchema]):
    email: str
    password: str

@dataclass
class AccessTokenQuery(BaseQuery[AccessTokenResponseSchema]):
    user_id: str

@dataclass
class GetCurrentUserQuery(BaseQuery[GetCurrentUserResponseSchema]):
    user_id: str
