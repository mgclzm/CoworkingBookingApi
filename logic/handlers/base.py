from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from logic.commands.base import BaseCommand
from logic.queries.base import BaseQuery, ResultT

CommandT = TypeVar('CommandT', bound=BaseCommand)

class CommandHandler(ABC, Generic[CommandT]):
    @abstractmethod
    async def handle(self, command: CommandT) -> None:
        ...

QueryT = TypeVar('QueryT', bound=BaseQuery)

class QueryHandler(ABC, Generic[QueryT, ResultT]):
    @abstractmethod
    async def handle(self, query: QueryT) -> ResultT:
        ... 