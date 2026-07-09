from dataclasses import dataclass

from api.routes.user.shemas import AccessTokenResponseSchema, RefreshTokenResponseSchema
from logic.queries.base import BaseQuery

@dataclass
class RefreshTokenQuery(BaseQuery[RefreshTokenResponseSchema]):
    email: str
    password: str

@dataclass
class AccessTokenQuery(BaseQuery[AccessTokenResponseSchema]):
    user_id: str