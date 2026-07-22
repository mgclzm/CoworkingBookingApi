from dataclasses import dataclass

from api.routes.workspace.schemas import (
    AddWorkplaceResponseSchema,
    RegisterWorkspaceResponseSchema,
    WorkspaceSchema,
)
from domain.entities.workspace import Workplace, Workspace, WorkspaceNotFoundError
from domain.values.workspace import (
    Number,
    Title,
    WorkingTime,
    WorkspaceDescription,
    WorkspaceLocation,
)
from logic.commands.workspace.workspace_commands import (
    AddWorkplaceCommand,
    PatchWorkspaceCommand,
    RegisterWorkspaceCommand,
)
from logic.handlers.base import CommandHandler, QueryHandler
from logic.queries.workspace.workspace_queries import (
    GetAllWorkspacesQuery,
    GetMyWorkspacesQuery,
)
from logic.uow.base import BaseUnitOfWork


@dataclass
class RegisterWorkspaceCommandHandler(
    CommandHandler[RegisterWorkspaceCommand, RegisterWorkspaceResponseSchema]
):
    _uow: BaseUnitOfWork

    async def handle(
        self, command: RegisterWorkspaceCommand
    ) -> RegisterWorkspaceResponseSchema:
        async with self._uow:
            location = WorkspaceLocation(city=command.city, street=command.street)
            working_time = WorkingTime(command.opening_time, command.closing_time)
            description = WorkspaceDescription(command.description)

            workspace = Workspace(
                location, working_time, description, owner_id=command.owner_id
            )
            await self._uow.workspace_repository.save(workspace)
            await self._uow.commit()

            response_schema = RegisterWorkspaceResponseSchema(
                workspace_id=workspace.workspace_id
            )
            return response_schema


@dataclass
class AddWorkplaceCommandHandler(
    CommandHandler[AddWorkplaceCommand, AddWorkplaceResponseSchema]
):
    _uow: BaseUnitOfWork

    async def handle(self, command: AddWorkplaceCommand) -> AddWorkplaceResponseSchema:
        async with self._uow:
            found_workspace = await self._uow.workspace_repository.find_by_workspace_id(
                command.workspace_id
            )
            if found_workspace is None:
                raise WorkspaceNotFoundError(command.workspace_id)

            found_workspace.ensure_owned_by(command.user_id)

            workplace_title = Title(command.title)
            workplace_number = Number(command.number)
            new_workplace = Workplace(workplace_title, workplace_number)

            found_workspace.register_workplace(new_workplace)

            await self._uow.workspace_repository.merge(found_workspace)
            await self._uow.commit()

            response_schema = AddWorkplaceResponseSchema(
                workplace_id=new_workplace.workplace_id,
                title=workplace_title.value,
                number=workplace_number.value,
            )
            return response_schema


@dataclass
class GetAllWorkspacesQueryHandler(
    QueryHandler[GetAllWorkspacesQuery, list[WorkspaceSchema]]
):
    _uow: BaseUnitOfWork

    async def handle(self, query: GetAllWorkspacesQuery) -> list[WorkspaceSchema]:
        async with self._uow:
            offset = (query.page_number - 1) * query.page_size
            limit = query.page_size
            workspaces = await self._uow.workspace_repository.find_all(
                limit=limit, offset=offset, city=query.city
            )

            response_schemas = [
                WorkspaceSchema.from_entity(workspace) for workspace in workspaces
            ]
            return response_schemas


@dataclass
class GetMyWorkspacesQueryHandler(
    QueryHandler[GetMyWorkspacesQuery, list[WorkspaceSchema]]
):
    _uow: BaseUnitOfWork

    async def handle(self, query: GetMyWorkspacesQuery) -> list[WorkspaceSchema]:
        async with self._uow:
            offset = (query.page_number - 1) * query.page_size
            limit = query.page_size
            workspaces = await self._uow.workspace_repository.find_all(
                limit=limit, offset=offset, owner_id=query.user_id
            )

            response_schemas = [
                WorkspaceSchema.from_entity(workspace) for workspace in workspaces
            ]
            return response_schemas


@dataclass
class PatchWorkspaceCommandHandler(CommandHandler[PatchWorkspaceCommand, None]):
    _uow: BaseUnitOfWork

    async def handle(self, command: PatchWorkspaceCommand) -> None:
        async with self._uow:
            workspace = await self._uow.workspace_repository.find_by_workspace_id(
                command.workspace_id
            )
            if workspace is None:
                raise WorkspaceNotFoundError(command.workspace_id)

            workspace.ensure_owned_by(command.user_id)

            workspace.update_location(city=command.city, street=command.street)
            workspace.update_working_time(
                opening_time=command.opening_time, closing_time=command.closing_time
            )
            workspace.update_description(command.description)

            await self._uow.workspace_repository.merge(workspace)
            await self._uow.commit()
