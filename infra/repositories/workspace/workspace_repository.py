from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from domain.entities.workspace import Workplace, Workspace
from domain.values.booking import BookingTime
from domain.values.workspace import Title, WorkingTime, WorkspaceDescription, Number
from infra.repositories.workspace.base import BaseWorkspaceRepository
from infra.repositories.workspace.workspace_model import WorkplaceModel, WorkspaceModel

def _convert_workplace_model_to_entity(workplace_model: WorkplaceModel) -> Workplace:
    title = Title(workplace_model.title)
    number = Number(workplace_model.number)
    is_active = workplace_model.is_active
    workplace_id = workplace_model.workplace_id
    return Workplace(title, number, is_active, workplace_id=workplace_id)

def _convert_workplace_entity_to_model(workplace_entity: Workplace) -> WorkplaceModel:
    workplace_id = workplace_entity.workplace_id
    title = workplace_entity.title.value
    number = workplace_entity.number.value
    is_active = workplace_entity.is_active
    return WorkplaceModel(workplace_id=workplace_id, title=title, 
                          number=number, is_active=is_active)

def _convert_workspace_entity_to_model(workspace_entity: Workspace) -> WorkspaceModel:
    workspace_id = workspace_entity.workspace_id
    opening_time = workspace_entity.working_time.opening_time
    closing_time = workspace_entity.working_time.closing_time
    description = workspace_entity.description.value
    is_active = workspace_entity.is_active
    workplaces = [_convert_workplace_entity_to_model(workplace) for workplace in workspace_entity._workplaces]
    return WorkspaceModel(workspace_id=workspace_id, opening_time=opening_time, closing_time=closing_time, 
                          description=description, is_active=is_active, workplaces=workplaces)

def _convert_workspace_model_to_entity(workspace_model: WorkspaceModel) -> Workspace:
    workspace_id = workspace_model.workspace_id
    workplaces = {_convert_workplace_model_to_entity(workplace) for workplace in workspace_model.workplaces}
    working_time = WorkingTime(workspace_model.opening_time, workspace_model.closing_time)
    description = WorkspaceDescription(workspace_model.description)
    is_active = workspace_model.is_active
    return Workspace(working_time, description, is_active, workspace_id=workspace_id, _workplaces=workplaces)

@dataclass
class SqlAlchemyWorkspaceRepository(BaseWorkspaceRepository):
    _session: AsyncSession

    async def save(self, entity: Workspace) -> None:
        workspace_model = _convert_workspace_entity_to_model(entity)
        self._session.add(workspace_model)

    async def delete(self, entity: Workspace) -> None:
        workspace_model = _convert_workspace_entity_to_model(entity)
        await self._session.delete(workspace_model)
    
    async def find_all(self) -> list[Workspace]:
        workspaces = await self._session.execute(select(WorkspaceModel).options(selectinload(WorkspaceModel.workplaces)))
        workspaces = workspaces.scalars().all()
        return [_convert_workspace_model_to_entity(workspace) for workspace in workspaces]
    
    async def find_by_workspace_id(self, workspace_id: str) -> Workspace | None:
        result = await self._session.execute(select(WorkspaceModel)
                                             .where(WorkspaceModel.workspace_id == workspace_id)
                                             .options(selectinload(WorkspaceModel.workplaces)))
        result = result.scalar_one_or_none()
        if not result:
            return None
        return _convert_workspace_model_to_entity(result)
    
    async def find_all_available_wokrplaces(self, workspace_id: str, booking_time: BookingTime) -> list[Workplace]:
        #TODO
        ...
        