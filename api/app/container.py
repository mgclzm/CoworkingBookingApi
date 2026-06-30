import punq

from functools import lru_cache

from logic.mediator.base import ICommandMediator
from logic.mediator.mediator import CommandMediator
from logic.uow.base import BaseUnitOfWork
from logic.uow.unit_of_work import SqlAlchemyUnitOfWork

@lru_cache(1)
def init_container() -> punq.Container:
    return _init_container()

def _init_container() -> punq.Container:
    container = punq.Container()

    container.register(BaseUnitOfWork, SqlAlchemyUnitOfWork)
    
    command_mediator = CommandMediator()
    
    container.register(ICommandMediator, CommandMediator)
    return container