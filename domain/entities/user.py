from dataclasses import dataclass, field
from datetime import datetime, time
from uuid import uuid4

from domain.values.user import Email, Name, Password

@dataclass(eq=False)
class AppUser:
    user_id: str = field(default_factory=lambda: str(uuid4()))
    name: Name = field(kw_only=True)
    email: Email = field(kw_only=True)
    password: Password = field(kw_only=True)
    creation_time: time = field(default_factory=lambda: datetime.now().time()) 
    is_active: bool = field(default=True)

    def __eq__(self, other: AppUser) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.user_id == other.user_id

    def __hash__(self) -> int:
        return hash(self.user_id)