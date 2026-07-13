from dataclasses import dataclass

from logic.commands.base import BaseCommand

@dataclass
class RegisterUserCommand(BaseCommand):
    first_name: str
    last_name: str
    email: str
    password: str

@dataclass
class LogoutCommand(BaseCommand):
    jti: str