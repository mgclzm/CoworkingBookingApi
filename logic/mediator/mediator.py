from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable

from domain.exceptions.errors import CommandHandlersNotFoundError, QueryHandlerNotFoundError
from logic.commands.base import BaseCommand
from logic.mediator.base import ICommandMediator, IQueryMediator
from logic.handlers.base import CommandHandler, QueryHandler
from logic.queries.base import BaseQuery, ResultT

@dataclass
class CommandMediator(ICommandMediator):
    _command_register: dict[type[BaseCommand], list[CommandHandler]] = field(default_factory=lambda: defaultdict(list), kw_only=True)

    def register_command(self, command_type: type[BaseCommand], handlers: Iterable[CommandHandler]) -> None:
        self._command_register[command_type].extend(handlers)
        
    async def execute_command(self, command: BaseCommand) -> None:
        command_type = type(command)
        handlers = self._command_register[command_type]
        if not handlers:
            raise CommandHandlersNotFoundError(f'There are no registered handlers for "{command_type}" command')
        for handler in handlers:
            await handler.handle(command)

@dataclass
class QueryMediator(IQueryMediator):
    _query_register: dict[type[BaseQuery], QueryHandler] = field(default_factory=dict, kw_only=True)

    def register_query(self, query_type: type[BaseQuery[ResultT]], handler: QueryHandler[BaseQuery[ResultT], ResultT]) -> None:
        self._query_register[query_type] = handler
    
    async def execute_query(self, query: BaseQuery[ResultT]) -> ResultT:
        query_type = type(query)
        handler = self._query_register.get(query_type)
        if not handler:
            raise QueryHandlerNotFoundError(f'Handler for "{query_type}" query not registered')
        return await handler.handle(query)
