from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Boolean 
from datetime import datetime

from infra.db.base import Base


class AppUserModel(Base):
    __tablename__ = 'users'

    user_id: Mapped[str] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(60), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    creation_time: Mapped[datetime] = mapped_column(DateTime)
    is_active: Mapped[bool] = mapped_column(Boolean)
