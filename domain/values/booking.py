from dataclasses import dataclass
from datetime import time

from domain.exceptions.errors import InvalidBookingTimeError

@dataclass(frozen=True)
class BookingTime:
    start_time: time
    end_time: time

    def __post_init__(self):
        if self.start_time >= self.end_time:
            raise InvalidBookingTimeError('Start time must be before end time')