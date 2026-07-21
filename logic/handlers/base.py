from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from logic.commands.base import BaseCommand, CommandResultT
from logic.queries.base import BaseQuery, QueryResultT

CommandT = TypeVar("CommandT", bound=BaseCommand)


class CommandHandler(ABC, Generic[CommandT, CommandResultT]):
    @abstractmethod
    async def handle(self, command: CommandT) -> CommandResultT: ...


QueryT = TypeVar("QueryT", bound=BaseQuery)


class QueryHandler(ABC, Generic[QueryT, QueryResultT]):
    @abstractmethod
    async def handle(self, query: QueryT) -> QueryResultT: ...
