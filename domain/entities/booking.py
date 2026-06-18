from dataclasses import dataclass, field
from uuid import uuid4
from enum import Enum

from domain.exceptions.errors import BookingCancelError, BookingConfirmError
from domain.values.booking import BookingTime

class BookingStatus(Enum):
    PENDING = 1
    CONFIRMED = 2
    CANCELLED = 3
    COMPLETED = 4

@dataclass
class Booking:
    booking_id: str = field(default_factory=lambda: str(uuid4()), kw_only=True)
    user_id: str
    workspace_id: str
    workplace_id: str
    booking_time: BookingTime
    status: BookingStatus = field(default=BookingStatus.PENDING)

    def confirm_booking(self) -> None:
        if self.status != BookingStatus.PENDING:
            raise BookingConfirmError('Cannot confirm not pending booking')
        self.status = BookingStatus.CONFIRMED
    
    def cancel_booking(self) -> None:
        if self.status == BookingStatus.COMPLETED or self.status == BookingStatus.CANCELLED:
            raise BookingCancelError('Cannot cancel completed booking')
        self.status = BookingStatus.CANCELLED
        