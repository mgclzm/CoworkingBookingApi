from dataclasses import dataclass

from api.routes.workspace.schemas import AddWorkplaceResponseSchema, RegisterWorkspaceResponseSchema
from domain.entities.workspace import Workplace, Workspace, WorkspaceNotFoundError
from domain.values.workspace import Title, Number, WorkingTime, WorkspaceDescription, WorkspaceLocation
from logic.commands.workspace.workspace_commands import AddWorkplaceCommand, RegisterWorkspaceCommand
from logic.handlers.base import CommandHandler
from logic.uow.base import BaseUnitOfWork

@dataclass
class RegisterWorkspaceCommandHandler(CommandHandler[RegisterWorkspaceCommand, RegisterWorkspaceResponseSchema]):
    _uow: BaseUnitOfWork

    async def handle(self, command: RegisterWorkspaceCommand) -> RegisterWorkspaceResponseSchema:
        async with self._uow:
            location = WorkspaceLocation(command.location)
            working_time = WorkingTime(command.opening_time, command.closing_time)
            description = WorkspaceDescription(command.description)

            workspace = Workspace(location, working_time, description, owner_id=command.owner_id)
            await self._uow.workspace_repository.save(workspace)
            await self._uow.commit()

            response_schema = RegisterWorkspaceResponseSchema(workspace_id=workspace.workspace_id,
                                                              owner_id=command.owner_id,
                                                              location=location.value,
                                                              description=description.value,
                                                              opening_time=working_time.opening_time,
                                                              closing_time=working_time.closing_time)
            return response_schema
        
@dataclass
class AddWorkplaceCommandHandler(CommandHandler[AddWorkplaceCommand, AddWorkplaceResponseSchema]):
    _uow: BaseUnitOfWork

    async def handle(self, command: AddWorkplaceCommand) -> AddWorkplaceResponseSchema:
        async with self._uow:
            found_workspace = await self._uow.workspace_repository.find_by_workspace_id(command.workspace_id)
            if found_workspace is None:
                raise WorkspaceNotFoundError(command.workspace_id)
            
            found_workspace.ensure_owned_by(command.user_id)
            
            workplace_title = Title(command.title)
            workplace_number = Number(command.number)
            new_workplace = Workplace(workplace_title, workplace_number)

            found_workspace.register_workplace(new_workplace)

            await self._uow.workspace_repository.merge(found_workspace)
            await self._uow.commit()

            response_schema = AddWorkplaceResponseSchema(workplace_id=new_workplace.workplace_id,
                                                         title=workplace_title.value,
                                                         number=workplace_number.value)
            return response_schema
