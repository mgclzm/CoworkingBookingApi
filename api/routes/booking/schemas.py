from datetime import date, time

from pydantic import BaseModel, Field

from infra.repositories.booking.booking_model import BookingModel
from infra.repositories.workspace.workspace_model import WorkplaceModel, WorkspaceModel


class CreateBookingSchema(BaseModel):
    start_time: time
    end_time: time
    day: date


class CreateBookingResponseSchema(BaseModel):
    booking_id: str


class GetMyBookingsQueryParams(BaseModel):
    page_number: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, gt=0, le=30)


class BookingSchema(BaseModel):
    booking_id: str
    workspace_city: str
    workspace_street: str
    workplace_title: str
    workplace_number: int
    start_time: time
    end_time: time
    day: date
    status: str

    @staticmethod
    def from_entities(
        booking: BookingModel, workspace: WorkspaceModel, workplace: WorkplaceModel
    ) -> "BookingSchema":
        return BookingSchema(
            booking_id=booking.booking_id,
            workspace_city=workspace.city,
            workspace_street=workspace.street,
            workplace_title=workplace.title,
            workplace_number=workplace.number,
            start_time=booking.start_time,
            end_time=booking.end_time,
            day=booking.day,
            status=booking.status,
        )
