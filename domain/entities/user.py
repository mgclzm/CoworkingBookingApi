from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from domain.values.user import Email, Name, Password

@dataclass(eq=False)
class AppUser:
    user_id: str = field(default_factory=lambda: str(uuid4()), kw_only=True)
    name: Name 
    email: Email 
    password: Password 
    creation_time: datetime = field(default_factory=lambda: datetime.now(), kw_only=True) 
    is_active: bool = field(default=True)

    def __eq__(self, other: AppUser) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.user_id == other.user_id

    def __hash__(self) -> int:
        return hash(self.user_id)