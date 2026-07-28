from dataclasses import dataclass

from taskiq_redis import RedisStreamBroker

from infra.task_broker.base import BaseTaskBroker


@dataclass
class RedisTaskBroker(BaseTaskBroker):
    broker: RedisStreamBroker

    async def startup(self) -> None:
        await self.broker.startup()

    async def shutdown(self) -> None:
        await self.broker.shutdown()
