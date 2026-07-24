from dataclasses import dataclass
from datetime import date, time

from domain.entities.base import ApplicationException, LogicException


@dataclass
class InvalidBookingTimeError(ApplicationException):
    start_time: time
    end_time: time

    @property
    def message(self) -> str:
        return f"Start time must be before end time, got start time = {self.start_time} end time = {self.end_time}"


@dataclass
class BookingConflictError(LogicException):
    start_time: time
    end_time: time
    day: date

    @property
    def message(self) -> str:
        return f'Booking conflict: requested time "start time - {self.start_time}, end_time - {self.end_time}, date - {self.day}" overlaps with existing booking'


@dataclass(frozen=True)
class BookingTime:
    start_time: time
    end_time: time
    day: date

    def __post_init__(self):
        if self.start_time >= self.end_time:
            raise InvalidBookingTimeError(
                start_time=self.start_time, end_time=self.end_time
            )
