from dataclasses import dataclass

from domain.entities.user import AppUser
from domain.exceptions.errors import EmailAlreadyExistError
from domain.values.user import Email, Name, Password
from logic.commands.user_commands import RegisterUserCommand
from logic.handlers.base import CommandHandler
from logic.uow.base import BaseUnitOfWork

from argon2 import PasswordHasher

@dataclass
class RegisterUserCommandHandler(CommandHandler[RegisterUserCommand]):
    _uow: BaseUnitOfWork

    async def handle(self, command: RegisterUserCommand) -> None:
        async with self._uow:
            if await self._uow.user_repository.find_by_email(command.email):
                raise EmailAlreadyExistError(f'Email address "{command.email}" already exist')
            
            user_name = Name(command.first_name, command.last_name)
            email = Email(command.email)
            ph = PasswordHasher()
            password = Password(ph.hash(command.password))
            new_user = AppUser(user_name, email, password)
            
            await self._uow.user_repository.save(new_user)
            await self._uow.commit()
