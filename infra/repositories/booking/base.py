from abc import abstractmethod

from api.routes.booking.schemas import BookingSchema
from domain.entities.booking import Booking
from domain.values.booking import BookingTime
from infra.repositories.base_repository import BaseRepository


class BaseBookingRepository(BaseRepository[Booking]):
    @abstractmethod
    async def find_all_by_user_id(
        self, user_id: str, *, limit: int = 10, offset: int = 0
    ) -> list[BookingSchema]: ...  # doubtful

    @abstractmethod
    async def is_workplace_available_for_booking(
        self, booking_time: BookingTime, workspace_id: str, workplace_number: int
    ) -> bool: ...

    @abstractmethod
    async def find_by_booking_id(self, booking_id: str) -> Booking | None: ...

    @abstractmethod
    async def bulk_update_expired_bookings(self) -> None: ...
