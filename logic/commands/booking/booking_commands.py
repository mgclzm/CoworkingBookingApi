from dataclasses import dataclass
from datetime import date, time

from api.routes.booking.schemas import CreateBookingResponseSchema
from logic.commands.base import BaseCommand


@dataclass(frozen=True)
class CreateBookingCommand(BaseCommand[CreateBookingResponseSchema]):
    user_id: str
    workspace_id: str
    workplace_number: int
    start_time: time
    end_time: time
    day: date


@dataclass(frozen=True)
class ConfirmBookingCommand(BaseCommand[None]):
    booking_id: str
    user_id: str
