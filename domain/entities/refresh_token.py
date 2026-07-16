from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from domain.entities.base import BaseEntity

@dataclass
class RefreshToken(BaseEntity):
    token_id: str = field(default_factory=lambda: str(uuid4()), kw_only=True)
    user_id: str
    expires_at: datetime
    revoked: bool = field(default=False)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc), kw_only=True)

    def __eq__(self, other: RefreshToken) -> bool:
        return self.token_id == other.token_id
    
    def __hash__(self) -> int:
        return hash(self.token_id)

    def is_valid(self) -> bool:
        return not self.revoked and datetime.now(timezone.utc) < self.expires_at
    
    def revoke(self) -> None:
        self.revoked = True 