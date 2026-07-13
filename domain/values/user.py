from dataclasses import dataclass
from email_validator import validate_email, EmailNotValidError

from domain.exceptions.errors import InvalidNameError, InvalidPasswordError

@dataclass(frozen=True)
class Name:
    first_name: str
    last_name: str

    def __post_init__(self):
        if not self.first_name.strip() or not self.last_name.strip():
            raise InvalidNameError('Firstname and lastname cannot be empty')
        if len(self.first_name) > 50 or len(self.last_name) > 50:
            raise InvalidNameError('Firstname and lastname length cannot be bigger then 50 characters')

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
            raise InvalidPasswordError('Password length cannot be bigger then 255 characters')
        