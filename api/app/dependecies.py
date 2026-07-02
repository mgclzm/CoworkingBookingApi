from fastapi import Depends

from api.app.container import init_container, typed_resolve
from logic.mediator.base import ICommandMediator

def get_command_mediator() -> ICommandMediator:
    container = init_container()
    return typed_resolve(container, ICommandMediator)