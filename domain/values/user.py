from dataclasses import dataclass
from email_validator import validate_email, EmailNotValidError

from domain.entities.base import ApplicationException

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


@dataclass(frozen=True)
class Name:
    first_name: str
    last_name: str

    def __post_init__(self):
        if not self.first_name.strip() or not self.last_name.strip():
            raise InvalidNameError(first_name=self.first_name, last_name=self.last_name)
        if len(self.first_name) > 50 or len(self.last_name) > 50:
            raise InvalidNameError(first_name=self.first_name, last_name=self.last_name)

@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        validate_email(self.value)
        if len(self.value) > 60:
            raise EmailNotValidError('Email cannot be bigger then 60 characters')

@dataclass(frozen=True)
class Password:
    value: str

    def __post_init__(self):
        if len(self.value) > 255:
            raise InvalidPasswordError(self.value)
        