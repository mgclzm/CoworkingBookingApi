from typing import Annotated
from urllib import response

from fastapi import APIRouter, Depends, HTTPException, status

from api.app.dependencies import get_command_mediator, require_access_token
from api.routes.user.security import AuthException
from api.routes.workspace.schemas import AddWorkplaceRequestSchema, AddWorkplaceResponseSchema, RegisterWorkspaceRequestSchema
from domain.entities.base import LogicException
from logic.commands.workspace.workspace_commands import AddWorkplaceCommand, RegisterWorkspaceCommand
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
                       status_code=status.HTTP_201_CREATED,
                       responses={
                           status.HTTP_201_CREATED: {'description': 'New workplace successfully registered',
                                                     'model': AddWorkplaceResponseSchema},
                           status.HTTP_401_UNAUTHORIZED: {'description': 'User in not authenticated'},
                           status.HTTP_403_FORBIDDEN: {'description': 'Authenticated user is not the owner of this workspace'},
                           status.HTTP_404_NOT_FOUND: {'description': ''}
                       },
                       summary='Endpoint to add workplace to an existing workspace, require access token')
async def add_workplace(workspace_id: str,
                        request_schema: AddWorkplaceRequestSchema,
                        command_mediator: Annotated[ICommandMediator, Depends(get_command_mediator)],
                        user_id: Annotated[str, Depends(require_access_token)]):
    add_workplace_command = AddWorkplaceCommand(user_id, workspace_id, request_schema.title, request_schema.number)
    try:
        response_schema = await command_mediator.execute_command(add_workplace_command)
    except LogicException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.message)
    except AuthException as ex:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ex.message)
    else:
        return response_schema
