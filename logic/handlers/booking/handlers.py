from dataclasses import dataclass

from api.routes.booking.schemas import BookingSchema, CreateBookingResponseSchema
from domain.entities.booking import Booking, BookingNotFoundError
from domain.entities.workspace import WorkplaceNotFoundError, WorkspaceNotFoundError
from domain.values.booking import BookingConflictError, BookingTime
from domain.values.workspace import Number
from infra.uow.base import BaseUnitOfWork
from logic.commands.booking.booking_commands import (
    CancelBookingCommand,
    ConfirmBookingCommand,
    CreateBookingCommand,
)
from logic.handlers.base import CommandHandler, QueryHandler
from logic.queries.booking.booking_queries import GetMyBookingsQuery


@dataclass
class CreateBookingCommandHandler(
    CommandHandler[CreateBookingCommand, CreateBookingResponseSchema]
):
    _uow: BaseUnitOfWork

    async def handle(
        self, command: CreateBookingCommand
    ) -> CreateBookingResponseSchema:
        async with self._uow:
            workspace = await self._uow.workspace_repository.find_by_workspace_id(
                command.workspace_id
            )
            if workspace is None:
                raise WorkspaceNotFoundError(command.workspace_id)

            workplace_number = Number(command.workplace_number)
            workplace = workspace.get_workplace(workplace_number)
            if workplace is None:
                raise WorkplaceNotFoundError(workplace_number.value)

            booking_time = BookingTime(
                command.start_time, command.end_time, command.day
            )
            if not await self._uow.booking_repository.is_workplace_available_for_booking(
                booking_time, command.workspace_id, command.workplace_number
            ):
                raise BookingConflictError(
                    command.start_time, command.end_time, command.day
                )

            new_booking = Booking(
                command.user_id,
                workspace.workspace_id,
                workplace.workplace_id,
                booking_time,
            )
            await self._uow.booking_repository.save(new_booking)
            await self._uow.commit()

            response_schema = CreateBookingResponseSchema(
                booking_id=new_booking.booking_id
            )
            return response_schema


@dataclass
class ConfirmBookingCommandHandler(CommandHandler[ConfirmBookingCommand, None]):
    _uow: BaseUnitOfWork

    async def handle(self, command: ConfirmBookingCommand) -> None:
        async with self._uow:
            found_booking = await self._uow.booking_repository.find_by_booking_id(
                command.booking_id
            )
            if found_booking is None:
                raise BookingNotFoundError(command.booking_id)

            found_booking.ensure_belong_to(command.user_id)

            found_booking.confirm_booking()

            await self._uow.booking_repository.merge(found_booking)
            await self._uow.commit()


@dataclass
class CancelBookingCommandHandler(CommandHandler[CancelBookingCommand, None]):
    _uow: BaseUnitOfWork

    async def handle(self, command: CancelBookingCommand) -> None:
        async with self._uow:
            found_booking = await self._uow.booking_repository.find_by_booking_id(
                command.booking_id
            )
            if found_booking is None:
                raise BookingNotFoundError(command.booking_id)

            found_booking.ensure_belong_to(command.user_id)

            found_booking.cancel_booking()

            await self._uow.booking_repository.merge(found_booking)
            await self._uow.commit()


@dataclass
class GetMyBookingsQueryHandler(QueryHandler[GetMyBookingsQuery, list[BookingSchema]]):
    _uow: BaseUnitOfWork

    async def handle(self, query: GetMyBookingsQuery) -> list[BookingSchema]:
        async with self._uow:
            offset = (query.page_number - 1) * query.page_size
            limit = query.page_size

            return await self._uow.booking_repository.find_all_by_user_id(
                query.user_id, limit=limit, offset=offset
            )
