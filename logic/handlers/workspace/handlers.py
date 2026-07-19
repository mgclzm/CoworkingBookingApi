from dataclasses import dataclass

from api.routes.workspace.schemas import RegisterWorkspaceResponseSchema
from domain.entities.workspace import Workspace
from domain.values.workspace import WorkingTime, WorkspaceDescription, WorkspaceLocation
from logic.commands.workspace.workspace_commands import RegisterWorkspaceCommand
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
