from datetime import date, time

from pydantic import BaseModel


class CreateBookingSchema(BaseModel):
    start_time: time
    end_time: time
    day: date


class CreateBookingResponseSchema(BaseModel):
    booking_id: str
