from dataclasses import dataclass

from api.routes.booking.schemas import BookingSchema
from logic.queries.base import BaseQuery


@dataclass(frozen=True)
class GetMyBookingsQuery(BaseQuery[list[BookingSchema]]):
    page_number: int
    page_size: int
    user_id: str
