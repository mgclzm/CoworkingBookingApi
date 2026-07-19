from typing import Annotated

from fastapi import APIRouter, Depends, status

from api.app.dependencies import get_command_mediator, require_access_token
from api.routes.workspace.schemas import RegisterWorkspaceRequestSchema
from logic.commands.workspace.workspace_commands import RegisterWorkspaceCommand
from logic.mediator.base import ICommandMediator

workspace_router = APIRouter(prefix='/v1', tags=['Workspace'])

@workspace_router.post('/workspace', 
                       status_code=status.HTTP_201_CREATED,
                       responses={
                           status.HTTP_201_CREATED: {'description': 'New workspace successfully registered'},
                           status.HTTP_401_UNAUTHORIZED: {'description': 'User is not authenticated'},
                       },
                       summary='Endpoint to register new workspace, require access token')
async def register_workspace(register_workspace_schema: RegisterWorkspaceRequestSchema, 
                             owner_id: Annotated[str, Depends(require_access_token)], 
                             command_mediator: Annotated[ICommandMediator, Depends(get_command_mediator)]):
    register_workspace_command = RegisterWorkspaceCommand(owner_id,
                                                          register_workspace_schema.opening_time,
                                                          register_workspace_schema.closing_time,
                                                          register_workspace_schema.location,
                                                          register_workspace_schema.description)
    response_schema = await command_mediator.execute_command(register_workspace_command)
    return response_schema

@workspace_router.post('/workspace/{workspace_id}/workplaces',
                       status_code=status.HTTP_200_OK,
                       responses={
                           status.HTTP_200_OK: {'description': 'New workplace successfully registered'},
                           status.HTTP_401_UNAUTHORIZED: {'description': 'User in not authenticated'}
                       },
                       summary='Endpoint to add workplace to an existing workspace, require access token')
async def add_workplace(_user_id: Annotated[str, Depends(require_access_token)]):
    ...
