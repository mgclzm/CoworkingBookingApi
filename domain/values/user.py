from dataclasses import dataclass
from email_validator import validate_email

from domain.exceptions.errors import InvalidNameError, InvalidPasswordError

@dataclass(frozen=True)
class Name:
    firstname: str
    lastname: str

    def __post_init__(self):
        if not self.firstname.strip() or not self.lastname.strip():
            raise InvalidNameError('Firstname and lastname cannot be empty')
        if len(self.firstname) > 50 or len(self.lastname) > 50:
            raise InvalidNameError('Firstname and lastname length cannot be bigger then 50 characters')

@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        validate_email(self.value)

@dataclass(frozen=True)
class Password:
    value: str

    def __post_init__(self):
        if len(self.value) > 255:
            raise InvalidPasswordError('Password lenght cannot be bigger then 255 characters')
        