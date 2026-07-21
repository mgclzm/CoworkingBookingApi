from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable

from domain.entities.base import ApplicationException
from logic.commands.base import BaseCommand, CommandResultT
from logic.mediator.base import ICommandMediator, IQueryMediator
from logic.handlers.base import CommandHandler, CommandT, QueryHandler, QueryT
from logic.queries.base import BaseQuery, QueryResultT

@dataclass
class CommandHandlerNotFoundError(ApplicationException):
    command_type: type[BaseCommand]

    @property
    def message(self) -> str:
        return f'There are no registered handlers for "{self.command_type}" command'

@dataclass
class QueryHandlerNotFoundError(ApplicationException):
    query_type: type[BaseQuery]

    @property
    def message(self) -> str:
        return f'Handler for "{self.query_type}" query not registered'

@dataclass
class CommandMediator(ICommandMediator):
    _command_register: dict[type[BaseCommand], CommandHandler] = field(default_factory=dict, kw_only=True)

    def register_command(self, command_type: type[CommandT], handler: CommandHandler[CommandT, CommandResultT]) -> None:
        self._command_register[command_type] = handler
        
    async def execute_command(self, command: BaseCommand[CommandResultT]) -> CommandResultT:
        command_type = type(command)
        handler = self._command_register.get(command_type)
        if not handler:
            raise CommandHandlerNotFoundError(command_type)
        return await handler.handle(command)

@dataclass
class QueryMediator(IQueryMediator):
    _query_register: dict[type[BaseQuery], QueryHandler] = field(default_factory=dict, kw_only=True)

    def register_query(self, query_type: type[QueryT], handler: QueryHandler[QueryT, QueryResultT]) -> None:
        self._query_register[query_type] = handler
    
    async def execute_query(self, query: BaseQuery[QueryResultT]) -> QueryResultT:
        query_type = type(query)
        handler = self._query_register.get(query_type)
        if not handler:
            raise QueryHandlerNotFoundError(query_type)
        return await handler.handle(query)
