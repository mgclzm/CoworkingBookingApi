from dataclasses import dataclass
from datetime import datetime

from domain.exceptions.errors import InvalidBookingTimeError

@dataclass(frozen=True)
class BookingTime:
    start_time: datetime
    end_time: datetime

    def __post_init__(self):
        if self.start_time >= self.end_time:
            raise InvalidBookingTimeError('Start time must be before end time')