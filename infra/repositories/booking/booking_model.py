from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from domain.entities.booking import BookingStatus
from infra.db.base import Base


class BookingModel(Base):
    __tablename__ = "booking"

    booking_id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))
    workspace_id: Mapped[str] = mapped_column(ForeignKey("workspaces.workspace_id"))
    workplace_id: Mapped[str] = mapped_column(ForeignKey("workplaces.workplace_id"))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(Enum(BookingStatus))
