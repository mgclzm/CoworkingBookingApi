from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Boolean, Time

from datetime import time

from infra.db.base import Base
from infra.repositories.user.user_model import AppUserModel

class WorkplaceModel(Base):
    __tablename__ = 'workplaces'

    workplace_id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    number: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean)

    workspace_id: Mapped[str] = mapped_column(ForeignKey('workspaces.workspace_id'))
    workspace: Mapped['WorkspaceModel'] = relationship(back_populates='workplaces')

class WorkspaceModel(Base):
    __tablename__ = 'workspaces'
    
    workspace_id: Mapped[str] = mapped_column(primary_key=True)
    opening_time: Mapped[time] = mapped_column(Time)
    closing_time: Mapped[time] = mapped_column(Time)
    location: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(1000))
    is_active: Mapped[bool] = mapped_column(Boolean)
    owner_id: Mapped[str] = mapped_column(ForeignKey('users.user_id'))

    workplaces: Mapped[list['WorkplaceModel']] = relationship(back_populates='workspace')