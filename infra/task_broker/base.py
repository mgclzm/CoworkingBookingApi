from abc import ABC, abstractmethod

from taskiq import AsyncBroker


class BaseTaskBroker(ABC):
    broker: AsyncBroker

    @abstractmethod
    async def startup(self) -> None: ...

    @abstractmethod
    async def shutdown(self) -> None: ...
