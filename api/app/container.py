from functools import cache
from typing import TypeVar, cast

import punq
from taskiq_redis import RedisStreamBroker

from infra.settings.settings import settings
from infra.task_broker.base import BaseTaskBroker
from infra.task_broker.redis_broker import RedisTaskBroker
from infra.uow.base import BaseUnitOfWork
from infra.uow.unit_of_work import SqlAlchemyUnitOfWork
from logic.commands.booking.booking_commands import (
    CancelBookingCommand,
    ConfirmBookingCommand,
    CreateBookingCommand,
)
from logic.commands.user.user_commands import (
    IssueRefreshTokenCommand,
    LogoutCommand,
    RegisterUserCommand,
)
from logic.commands.workspace.workspace_commands import (
    AddWorkplaceCommand,
    PatchWorkplaceCommand,
    PatchWorkspaceCommand,
    RegisterWorkspaceCommand,
)
from logic.handlers.booking.handlers import (
    CancelBookingCommandHandler,
    ConfirmBookingCommandHandler,
    CreateBookingCommandHandler,
    GetMyBookingsQueryHandler,
)
from logic.handlers.user.handlers import (
    AccessTokenQueryHandler,
    GetCurrentUserQueryHandler,
    IssueRefreshTokenCommandHandler,
    LogoutCommandHandler,
    RegisterUserCommandHandler,
)
from logic.handlers.workspace.handlers import (
    AddWorkplaceCommandHandler,
    GetAllWorkspacesQueryHandler,
    GetMyWorkspacesQueryHandler,
    PatchWorkplaceCommandHandler,
    PatchWorkspaceCommandHandler,
    RegisterWorkspaceCommandHandler,
)
from logic.mediator.base import ICommandMediator, IQueryMediator
from logic.mediator.mediator import CommandMediator, QueryMediator
from logic.queries.booking.booking_queries import GetMyBookingsQuery
from logic.queries.user.user_queries import AccessTokenQuery, GetCurrentUserQuery
from logic.queries.workspace.workspace_queries import (
    GetAllWorkspacesQuery,
    GetMyWorkspacesQuery,
)

COMMAND_AND_HANDLER_PAIRS = [
    (RegisterUserCommand, RegisterUserCommandHandler),
    (IssueRefreshTokenCommand, IssueRefreshTokenCommandHandler),
    (LogoutCommand, LogoutCommandHandler),
    (RegisterWorkspaceCommand, RegisterWorkspaceCommandHandler),
    (AddWorkplaceCommand, AddWorkplaceCommandHandler),
    (PatchWorkspaceCommand, PatchWorkspaceCommandHandler),
    (PatchWorkplaceCommand, PatchWorkplaceCommandHandler),
    (CreateBookingCommand, CreateBookingCommandHandler),
    (ConfirmBookingCommand, ConfirmBookingCommandHandler),
    (CancelBookingCommand, CancelBookingCommandHandler),
]

QUERY_AND_HANDLER_PAIRS = [
    (AccessTokenQuery, AccessTokenQueryHandler),
    (GetCurrentUserQuery, GetCurrentUserQueryHandler),
    (GetAllWorkspacesQuery, GetAllWorkspacesQueryHandler),
    (GetMyWorkspacesQuery, GetMyWorkspacesQueryHandler),
    (GetMyBookingsQuery, GetMyBookingsQueryHandler),
]


def _init_command_mediator(container: punq.Container) -> CommandMediator:
    command_mediator = CommandMediator()
    for command_type, handler_type in COMMAND_AND_HANDLER_PAIRS:
        handler = typed_resolve(container, handler_type)
        command_mediator.register_command(command_type, handler)
    return command_mediator


def _init_query_mediator(container: punq.Container) -> QueryMediator:
    query_mediator = QueryMediator()
    for query_type, handler_type in QUERY_AND_HANDLER_PAIRS:
        handler = typed_resolve(container, handler_type)
        query_mediator.register_query(query_type, handler)
    return query_mediator


def _init_redis_task_broker() -> RedisTaskBroker:
    task_broker = RedisTaskBroker(broker=RedisStreamBroker(url=settings.redis_url))
    return task_broker


T = TypeVar("T")


def typed_resolve(container: punq.Container, service_type: type[T]) -> T:
    return cast(T, container.resolve(service_type))


@cache
def init_container() -> punq.Container:
    return _init_container()


def _init_container() -> punq.Container:
    container = punq.Container()

    container.register(BaseUnitOfWork, SqlAlchemyUnitOfWork, scope=punq.Scope.transient)

    container.register(RegisterUserCommandHandler)
    container.register(IssueRefreshTokenCommandHandler)
    container.register(LogoutCommandHandler)
    container.register(RegisterWorkspaceCommandHandler)
    container.register(AddWorkplaceCommandHandler)
    container.register(PatchWorkspaceCommandHandler)
    container.register(PatchWorkplaceCommandHandler)
    container.register(CreateBookingCommandHandler)
    container.register(ConfirmBookingCommandHandler)
    container.register(CancelBookingCommandHandler)

    container.register(AccessTokenQueryHandler)
    container.register(GetCurrentUserQueryHandler)
    container.register(GetAllWorkspacesQueryHandler)
    container.register(GetMyWorkspacesQueryHandler)
    container.register(GetMyBookingsQueryHandler)

    container.register(
        ICommandMediator,
        factory=lambda: _init_command_mediator(container),
        scope=punq.Scope.transient,
    )
    container.register(
        IQueryMediator,
        factory=lambda: _init_query_mediator(container),
        scope=punq.Scope.transient,
    )

    container.register(
        BaseTaskBroker,
        factory=_init_redis_task_broker,
        scope=punq.Scope.singleton,
    )

    # container.register(Redis, factory=_init_redis_cache, scope=punq.Scope.singleton)
    return container
