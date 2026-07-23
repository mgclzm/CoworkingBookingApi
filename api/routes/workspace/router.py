from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.app.dependencies import (
    get_command_mediator,
    get_query_mediator,
    require_access_token,
)
from api.routes.workspace.schemas import (
    AddWorkplaceRequestSchema,
    AddWorkplaceResponseSchema,
    GetWorkplacesParams,
    PatchWorkplaceSchema,
    PatchWorkspaceSchema,
    RegisterWorkspaceRequestSchema,
    WorkspaceSchema,
)
from domain.entities.base import ApplicationException, LogicException
from domain.entities.workspace import WorkplaceNotFoundError
from logic.commands.workspace.workspace_commands import (
    AddWorkplaceCommand,
    PatchWorkplaceCommand,
    PatchWorkspaceCommand,
    RegisterWorkspaceCommand,
)
from logic.mediator.base import ICommandMediator, IQueryMediator
from logic.queries.workspace.workspace_queries import (
    GetAllWorkspacesQuery,
    GetMyWorkspacesQuery,
)

workspace_router = APIRouter(prefix="/v1", tags=["Workspace"])


@workspace_router.post(
    "/workspace",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "New workspace successfully registered"
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "User is not authenticated"},
    },
    summary="Endpoint to register new workspace, require access token",
)
async def register_workspace(
    register_workspace_schema: RegisterWorkspaceRequestSchema,
    owner_id: Annotated[str, Depends(require_access_token)],
    command_mediator: Annotated[ICommandMediator, Depends(get_command_mediator)],
):
    register_workspace_command = RegisterWorkspaceCommand(
        owner_id,
        register_workspace_schema.opening_time,
        register_workspace_schema.closing_time,
        register_workspace_schema.city,
        register_workspace_schema.street,
        register_workspace_schema.description,
    )
    response_schema = await command_mediator.execute_command(register_workspace_command)
    return response_schema


@workspace_router.post(
    "/workspace/{workspace_id}/workplaces",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "New workplace successfully registered",
            "model": AddWorkplaceResponseSchema,
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "User in not authenticated"},
        status.HTTP_403_FORBIDDEN: {
            "description": "Authenticated user is not the owner of this workspace"
        },
        status.HTTP_404_NOT_FOUND: {"description": "Workspace not found"},
    },
    summary="Endpoint to add workplace to an existing workspace, require access token",
)
async def add_workplace(
    workspace_id: str,
    request_schema: AddWorkplaceRequestSchema,
    command_mediator: Annotated[ICommandMediator, Depends(get_command_mediator)],
    user_id: Annotated[str, Depends(require_access_token)],
):
    add_workplace_command = AddWorkplaceCommand(
        user_id, workspace_id, request_schema.title, request_schema.number
    )
    try:
        response_schema = await command_mediator.execute_command(add_workplace_command)
    except ApplicationException as ex:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ex.message)
    except LogicException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.message)
    else:
        return response_schema


@workspace_router.get(
    "/workspace",
    status_code=status.HTTP_200_OK,
    response_model=list[WorkspaceSchema],
    responses={
        status.HTTP_200_OK: {"description": "Return information about workspaces"},
    },
    summary="Endpoint to obtain information about workspaces",
)
async def get_all_workplaces(
    query_mediator: Annotated[IQueryMediator, Depends(get_query_mediator)],
    query_params: Annotated[GetWorkplacesParams, Query()],
):
    get_all_workspaces_query = GetAllWorkspacesQuery(
        query_params.page_number, query_params.page_size, query_params.city
    )
    response_schemas = await query_mediator.execute_query(get_all_workspaces_query)
    return response_schemas


@workspace_router.get(
    "/me/workspace",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Return information about workspaces owned by authenticated user"
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "User is not authenticated"},
    },
    summary="Endpoint to obtain information about workspaces, owned by current user, require access token",
)
async def get_my_workspaces(
    user_id: Annotated[str, Depends(require_access_token)],
    query_mediator: Annotated[IQueryMediator, Depends(get_query_mediator)],
    query_params: Annotated[GetWorkplacesParams, Query()],
):
    get_my_workspaces_query = GetMyWorkspacesQuery(
        user_id, query_params.page_number, query_params.page_size
    )
    response_schemas = await query_mediator.execute_query(get_my_workspaces_query)
    return response_schemas


@workspace_router.patch(
    "/workspace/{workspace_id}",
    responses={
        status.HTTP_200_OK: {"description": "Workspace parameter successfully changed"},
        status.HTTP_401_UNAUTHORIZED: {"description": "User is not authenticated"},
        status.HTTP_403_FORBIDDEN: {
            "description": "Authenticated user is not the owner of this workspace"
        },
        status.HTTP_404_NOT_FOUND: {"description": "Workspace not found"},
    },
    summary="Endpoint to change some parameters in workspace",
)
async def patch_workspace(
    workspace_id: str,
    patch_workspace_schema: PatchWorkspaceSchema,
    user_id: Annotated[str, Depends(require_access_token)],
    command_mediator: Annotated[ICommandMediator, Depends(get_command_mediator)],
):
    patch_workspace_command = PatchWorkspaceCommand(
        workspace_id,
        user_id,
        patch_workspace_schema.city,
        patch_workspace_schema.street,
        patch_workspace_schema.opening_time,
        patch_workspace_schema.closing_time,
        patch_workspace_schema.description,
    )
    try:
        await command_mediator.execute_command(patch_workspace_command)
    except ApplicationException as ex:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ex.message)
    except LogicException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.message)


@workspace_router.patch(
    "/workspace/{workspace_id}/workplaces/{workplace_number}",
    responses={
        status.HTTP_200_OK: {"description": "Workplace parameter successfully changed"},
        status.HTTP_401_UNAUTHORIZED: {"description": "User is not authenticated"},
        status.HTTP_403_FORBIDDEN: {
            "description": "Authenticated user is not the owner of this workspace"
        },
        status.HTTP_404_NOT_FOUND: {"description": "Workspace not found"},
        status.HTTP_409_CONFLICT: {"description": "New workplace number already taken"},
    },
    summary="Endpoint to change some parameters in workplace",
)
async def patch_workplace(
    workspace_id: str,
    workplace_number: int,
    patch_workplace_schema: PatchWorkplaceSchema,
    user_id: Annotated[str, Depends(require_access_token)],
    command_mediator: Annotated[ICommandMediator, Depends(get_command_mediator)],
):
    patch_workplace_command = PatchWorkplaceCommand(
        workspace_id,
        user_id,
        workplace_number,
        patch_workplace_schema.number,
        patch_workplace_schema.title,
    )
    try:
        await command_mediator.execute_command(patch_workplace_command)
    except ApplicationException as ex:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ex.message)
    except LogicException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
            if isinstance(ex, WorkplaceNotFoundError)
            else status.HTTP_409_CONFLICT,
            detail=ex.message,
        )
