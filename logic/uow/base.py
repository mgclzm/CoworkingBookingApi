from abc import ABC, abstractmethod
from types import TracebackType
from typing import Type

class BaseUnitOfWork(ABC):
    @abstractmethod
    async def __aenter__(self):
        ...
    
    @abstractmethod
    async def __aexit__(self, exc_type: Type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None):
        ...
    
    @abstractmethod
    async def commit(self):
        ...
    
    # @abstractmethod
    # async def _rollback(self):
    #     ...