from dataclasses import dataclass, field
from uuid import uuid4
from enum import Enum

from domain.entities.base import ApplicationException, BaseEntity
from domain.values.booking import BookingTime

class BookingStatus(str, Enum):
    PENDING = 'PENDING'
    CONFIRMED = 'CONFIRMED'
    CANCELLED = 'CANCELLED'
    COMPLETED = 'COMPLETED'

@dataclass
class BookingConfirmError(ApplicationException):
    @property
    def message(self) -> str:
        return 'Cannot confirm not pending booking'
    
@dataclass
class BookingCancelError(ApplicationException):
    @property
    def message(self) -> str:
        return 'Cannot cancel completed booking'

@dataclass
class Booking(BaseEntity):
    booking_id: str = field(default_factory=lambda: str(uuid4()), kw_only=True)
    user_id: str
    workspace_id: str
    workplace_id: str
    booking_time: BookingTime
    status: BookingStatus = field(default=BookingStatus.PENDING)

    def confirm_booking(self) -> None:
        if self.status != BookingStatus.PENDING:
            raise BookingConfirmError()
        self.status = BookingStatus.CONFIRMED
    
    def cancel_booking(self) -> None:
        if self.status == BookingStatus.COMPLETED or self.status == BookingStatus.CANCELLED:
            raise BookingCancelError()
        self.status = BookingStatus.CANCELLED
        