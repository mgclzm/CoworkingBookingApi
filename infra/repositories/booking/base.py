from abc import abstractmethod

from domain.entities.booking import Booking
from domain.values.booking import BookingTime
from infra.repositories.base_repository import BaseRepository


class BaseBookingRepository(BaseRepository[Booking]):
    @abstractmethod
    async def find_all_by_user_id(self, user_id: str) -> list[Booking]: ...

    async def is_workplace_available_for_booking(
        self, booking_time: BookingTime, workspace_id: str, workplace_number: int
    ) -> bool: ...
