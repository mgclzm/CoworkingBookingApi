from typing import Annotated

from taskiq import TaskiqDepends, TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource

from api.app.container import init_container, typed_resolve
from infra.task_broker.base import BaseTaskBroker
from infra.uow.base import BaseUnitOfWork

container = init_container()

broker = typed_resolve(container, BaseTaskBroker).broker
scheduler = TaskiqScheduler(broker, [LabelScheduleSource(broker)])


def get_uow() -> BaseUnitOfWork:
    return typed_resolve(container, BaseUnitOfWork)


@broker.task(
    task_name="expire_bookings",
    schedule=[{"cron": "*/5 * * * *"}],
)
async def mark_expire_bookings(
    uow: Annotated[BaseUnitOfWork, TaskiqDepends(get_uow)],
) -> None:
    async with uow:
        await uow.booking_repository.bulk_update_expired_bookings()
        await uow.commit()


@broker.task(task_name="revoke_expired_tokens", schedule=[{"cron": "*/5 * * * *"}])
async def mark_revoked_expired_tokens(
    uow: Annotated[BaseUnitOfWork, TaskiqDepends(get_uow)],
) -> None:
    async with uow:
        await uow.refresh_token_repository.bulk_update_expired_tokens()
        await uow.commit()
