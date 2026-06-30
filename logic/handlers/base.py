from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from logic.commands.base import BaseCommand
from logic.queries.base import BaseQuery, ResultT

class CommandHandler(ABC):
    @abstractmethod
    async def handle(self, command: BaseCommand) -> None:
        ...

QueryT = TypeVar('QueryT', bound=BaseQuery)

class QueryHandler(ABC, Generic[QueryT, ResultT]):
    @abstractmethod
    async def handle(self, query: QueryT) -> ResultT:
        ... 