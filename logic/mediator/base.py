from abc import ABC, abstractmethod

from logic.commands.base import BaseCommand, CommandResultT
from logic.handlers.base import CommandHandler, QueryHandler
from logic.queries.base import BaseQuery, QueryResultT


class ICommandMediator(ABC):
    @abstractmethod
    def register_command(
        self,
        command_type: type[BaseCommand[CommandResultT]],
        handler: CommandHandler[BaseCommand[CommandResultT], CommandResultT],
    ) -> None: ...

    @abstractmethod
    async def execute_command(
        self, command: BaseCommand[CommandResultT]
    ) -> CommandResultT: ...


class IQueryMediator(ABC):
    @abstractmethod
    def register_query(
        self,
        query_type: type[BaseQuery[QueryResultT]],
        handler: QueryHandler[BaseQuery[QueryResultT], QueryResultT],
    ) -> None: ...

    @abstractmethod
    async def execute_query(self, query: BaseQuery[QueryResultT]) -> QueryResultT: ...
