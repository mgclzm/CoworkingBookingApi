from abc import ABC, abstractmethod
from logic.handlers.base import CommandHandler, QueryHandler
from logic.commands.base import BaseCommand
from logic.queries.base import BaseQuery, ResultT

class ICommandBus(ABC):
    @abstractmethod
    def register_command(self, command_type: type[BaseCommand], handler: CommandHandler) -> None:
        ... 
    
    @abstractmethod
    async def execute_command(self, command: BaseCommand) -> None:
        ...

class IQueryBus(ABC):
    @abstractmethod
    def register_query(self, query_type: type[BaseQuery[ResultT]], handler: QueryHandler[BaseQuery[ResultT], ResultT]) -> None:
        ...
    
    @abstractmethod
    async def execute_query(self, query: BaseQuery[ResultT]) -> ResultT:
        ...