from dataclasses import dataclass
from datetime import datetime

from domain.entities.booking import InvalidBookingTimeError

@dataclass(frozen=True)
class BookingTime:
    start_time: datetime
    end_time: datetime

    def __post_init__(self):
        if self.start_time >= self.end_time:
            raise InvalidBookingTimeError(start_time=self.start_time, end_time=self.end_time)