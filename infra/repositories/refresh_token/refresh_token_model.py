from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from infra.db.base import Base


class RefreshTokenModel(Base):
    __tablename__ = "refresh_tokens"

    token_id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"), index=True)
    expires_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), index=True)
    revoked: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
