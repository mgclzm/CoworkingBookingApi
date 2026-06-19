from abc import abstractmethod

from domain.entities.booking import Booking, BookingStatus
from domain.entities.user import AppUser
from infra.repositories.base_repository import BaseRepository

class BaseBookingRepository(BaseRepository[Booking]):
    @abstractmethod
    async def find_all_by_user_id(self, user_id: str) -> list[Booking]:
        ...
    
