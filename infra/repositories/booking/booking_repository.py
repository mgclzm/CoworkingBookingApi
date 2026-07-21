from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.booking import Booking, BookingStatus
from domain.values.booking import BookingTime
from infra.repositories.booking.base import BaseBookingRepository
from infra.repositories.booking.booking_model import BookingModel


def _convert_booking_model_to_entity(booking_model: BookingModel) -> Booking:
    user_id = booking_model.user_id
    workspace_id = booking_model.workspace_id
    workplace_id = booking_model.workplace_id
    booking_time = BookingTime(booking_model.start_time, booking_model.end_time)
    status = BookingStatus(booking_model.status)
    booking_id = booking_model.booking_id
    return Booking(
        user_id, workspace_id, workplace_id, booking_time, status, booking_id=booking_id
    )


def _convert_booking_entity_to_model(booking_entity: Booking) -> BookingModel:
    booking_id = booking_entity.booking_id
    user_id = booking_entity.user_id
    workspace_id = booking_entity.workspace_id
    workplace_id = booking_entity.workplace_id
    start_time = booking_entity.booking_time.start_time
    end_time = booking_entity.booking_time.end_time
    status = booking_entity.status.value
    return BookingModel(
        booking_id=booking_id,
        user_id=user_id,
        workspace_id=workspace_id,
        workplace_id=workplace_id,
        start_time=start_time,
        end_time=end_time,
        status=status,
    )


@dataclass
class SqlAlchemyBookingRepository(BaseBookingRepository):
    _session: AsyncSession

    async def save(self, entity: Booking) -> None:
        booking_model = _convert_booking_entity_to_model(entity)
        self._session.add(booking_model)

    async def delete(self, entity: Booking) -> None:
        booking_model = _convert_booking_entity_to_model(entity)
        await self._session.delete(booking_model)

    async def merge(self, entity: Booking) -> None:
        booking_model = _convert_booking_entity_to_model(entity)
        await self._session.merge(booking_model)

    async def find_all_by_user_id(self, user_id: str) -> list[Booking]:
        result = await self._session.execute(
            select(BookingModel).where(BookingModel.user_id == user_id)
        )
        result = result.scalars().all()
        return [_convert_booking_model_to_entity(booking) for booking in result]
