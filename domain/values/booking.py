from dataclasses import dataclass
from datetime import datetime

from domain.entities.base import ApplicationException


@dataclass
class InvalidBookingTimeError(ApplicationException):
    start_time: datetime
    end_time: datetime

    @property
    def message(self) -> str:
        return f"Start time must be before end time, got start time = {self.start_time} end time = {self.end_time}"


@dataclass(frozen=True)
class BookingTime:
    start_time: datetime
    end_time: datetime

    def __post_init__(self):
        if self.start_time >= self.end_time:
            raise InvalidBookingTimeError(
                start_time=self.start_time, end_time=self.end_time
            )
