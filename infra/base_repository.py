from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):

    @abstractmethod
    async def save(self, entity: T) -> None:
        ...
    
    @abstractmethod
    async def delete(self, entity: T) -> None:
        ...