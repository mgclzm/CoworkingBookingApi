from typing import TypeVar, cast

import punq

from functools import lru_cache

from logic.commands.base import BaseCommand
from logic.commands.user_commands import RegisterUserCommand
from logic.handlers.base import CommandHandler
from logic.handlers.user.handlers import RegisterUserCommandHandler
from logic.mediator.base import ICommandMediator
from logic.mediator.mediator import CommandMediator
from logic.uow.base import BaseUnitOfWork
from logic.uow.unit_of_work import SqlAlchemyUnitOfWork

COMMAND_AND_HANDLERS_PAIRS = [
    (RegisterUserCommand, [RegisterUserCommandHandler]),
]

def _init_command_mediator(container: punq.Container) -> CommandMediator:
    command_mediator = CommandMediator()
    for command_type, handler_types in COMMAND_AND_HANDLERS_PAIRS:
        handlers = [typed_resolve(container, handler_type) for handler_type in handler_types]
        command_mediator.register_command(command_type, handlers)
    return command_mediator

T = TypeVar('T')
def typed_resolve(container: punq.Container, service_type: type[T]) -> T:
    return cast(T, container.resolve(service_type))

@lru_cache(maxsize=None)
def init_container() -> punq.Container:
    return _init_container()

def _init_container() -> punq.Container:
    container = punq.Container()

    container.register(BaseUnitOfWork, SqlAlchemyUnitOfWork, scope=punq.Scope.singleton)
    
    container.register(RegisterUserCommandHandler)

    container.register(ICommandMediator, factory=lambda: _init_command_mediator(container), scope=punq.Scope.singleton)
    return container