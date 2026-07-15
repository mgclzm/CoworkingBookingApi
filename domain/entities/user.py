from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from domain.entities.base import ApplicationException, BaseEntity, LogicException
from domain.values.user import Email, Name, Password

@dataclass
class InvalidNameError(ApplicationException):
    first_name: str
    last_name: str

    @property
    def message(self) -> str:
        return f'First name and last name cannot be empty or bigger then 50 characters, got first name = {self.first_name} last name = {self.last_name}'

@dataclass
class InvalidPasswordError(ApplicationException):
    password_value: str

    @property
    def message(self) -> str:
        return f'Password length cannot be bigger then 255 characters, got {len(self.password_value)}'

@dataclass
class EmailAlreadyExistError(LogicException):
    email: str

    @property
    def message(self) -> str:
        return f'Email address "{self.email}" already exist'

@dataclass
class UserNotFoundError(LogicException):
    user_id: str = field(default='')
    email: str = field(default='')
    first_name: str = field(default='')
    last_name: str = field(default='')

    @property
    def message(self) -> str:
        return f'User with "{self.user_id}" id, "{self.email}" email address, "{self.first_name}" first_name, "{self.last_name}" last name not found' #doubtful

@dataclass
class InvalidUserCredentialsError(LogicException):
    @property
    def message(self) -> str:
        return 'Invalid user credentials'

@dataclass(eq=False)
class AppUser(BaseEntity):
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