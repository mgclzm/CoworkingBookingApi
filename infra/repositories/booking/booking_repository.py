from dataclasses import dataclass

from sqlalchemy import and_, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.routes.booking.schemas import BookingSchema
from domain.entities.booking import Booking, BookingStatus
from domain.values.booking import BookingTime
from infra.repositories.booking.base import BaseBookingRepository
from infra.repositories.booking.booking_model import BookingModel
from infra.repositories.workspace.workspace_model import WorkplaceModel, WorkspaceModel


def _convert_booking_model_to_entity(booking_model: BookingModel) -> Booking:
    user_id = booking_model.user_id
    workspace_id = booking_model.workspace_id
    workplace_id = booking_model.workplace_id
    booking_time = BookingTime(
        booking_model.start_time, booking_model.end_time, booking_model.day
    )
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
    day = booking_entity.booking_time.day
    status = booking_entity.status.value
    return BookingModel(
        booking_id=booking_id,
        user_id=user_id,
        workspace_id=workspace_id,
        workplace_id=workplace_id,
        start_time=start_time,
        end_time=end_time,
        day=day,
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

    async def find_all_by_user_id(
        self, user_id: str, *, limit: int = 10, offset: int = 0
    ) -> list[BookingSchema]:
        query = (
            select(BookingModel, WorkspaceModel, WorkplaceModel)
            .join(
                WorkspaceModel, BookingModel.workspace_id == WorkspaceModel.workspace_id
            )
            .join(
                WorkplaceModel, BookingModel.workplace_id == WorkplaceModel.workplace_id
            )
            .where(BookingModel.user_id == user_id)
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(query)
        return [
            BookingSchema.from_entities(booking, workspace, workplace)
            for booking, workspace, workplace in result
        ]

    async def is_workplace_available_for_booking(
        self, booking_time: BookingTime, workspace_id: str, workplace_number: int
    ) -> bool:
        overlap = and_(
            BookingModel.start_time < booking_time.end_time,
            BookingModel.end_time > booking_time.start_time,
        )
        query = (
            select(BookingModel)
            .join(
                WorkplaceModel, BookingModel.workspace_id == WorkplaceModel.workspace_id
            )
            .where(
                WorkplaceModel.workspace_id == workspace_id,
                WorkplaceModel.number == workplace_number,
                BookingModel.day == booking_time.day,
                BookingModel.status == BookingStatus.CONFIRMED,
                overlap,
            )
            .limit(1)
        )
        result = await self._session.execute(query)
        return result.scalar_one_or_none() is None

    async def find_by_booking_id(self, booking_id: str) -> Booking | None:
        result = await self._session.execute(
            select(BookingModel).where(BookingModel.booking_id == booking_id)
        )
        result = result.scalar_one_or_none()
        if result is None:
            return None
        return _convert_booking_model_to_entity(result)

    async def bulk_update_expired_bookings(self) -> None:

        query = (
            update(BookingModel)
            .where((BookingModel.day + BookingModel.end_time) < func.now())
            .where(BookingModel.status != BookingStatus.COMPLETED)
            .values(status=BookingStatus.COMPLETED)
        )
        await self._session.execute(query)
