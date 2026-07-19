from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api.routes.user.security import AuthException, RefreshTokenData

from api.app.dependencies import get_command_mediator, get_query_mediator, require_access_token, require_refresh_token
from api.routes.user.schemas import (AccessTokenResponseSchema, 
                                     GetCurrentUserResponseSchema, 
                                     IssueRefreshTokenResponseSchema, 
                                     RegisterUserResponseSchema, 
                                     RegisterUserSchema)
from domain.entities.base import LogicException
from logic.commands.user.user_commands import LogoutCommand, RegisterUserCommand, IssueRefreshTokenCommand
from logic.mediator.base import ICommandMediator, IQueryMediator
from logic.queries.user.user_queries import AccessTokenQuery, GetCurrentUserQuery

user_router = APIRouter(prefix='/v1', tags=['App user'])

@user_router.post('/user/registration',
                  status_code=status.HTTP_201_CREATED,
                  responses={
                      status.HTTP_201_CREATED: {'description': 'User successfully registered',
                                                'model': RegisterUserResponseSchema}, 
                      status.HTTP_409_CONFLICT: {'description': 'User registration was unsuccessful'}
                  },
                  summary='Public endpoint for user registration')
async def register_user(register_user_schema: RegisterUserSchema, 
                        command_mediator: Annotated[ICommandMediator, Depends(get_command_mediator)]):
    first_name = register_user_schema.first_name
    last_name = register_user_schema.last_name
    email = register_user_schema.email
    password = register_user_schema.password
    register_user_command = RegisterUserCommand(first_name, last_name, email, password)
    try:
        response_schema = await command_mediator.execute_command(register_user_command)
    except LogicException as ex:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=ex.message) from ex
    else:
        return response_schema

@user_router.post('/login', 
                  status_code=status.HTTP_200_OK, 
                  responses={
                      status.HTTP_200_OK: {'description': 'Return new refresh and access token pair'},
                      status.HTTP_401_UNAUTHORIZED: {'description': 'User is not registered, or the data provided is incorrect'}
                  },
                  response_model=IssueRefreshTokenResponseSchema,
                  summary='Endpoint to obtain refresh token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                command_mediator: Annotated[ICommandMediator, Depends(get_command_mediator)]):
    issue_refresh_token_command = IssueRefreshTokenCommand(form_data.username, form_data.password)
    try:
        response_schema = await command_mediator.execute_command(issue_refresh_token_command) 
    except LogicException as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ex.message) from ex
    else:
        return response_schema

@user_router.post('/refresh',
                  status_code=status.HTTP_200_OK,
                  response_model=AccessTokenResponseSchema,
                  responses={
                      status.HTTP_200_OK: {'description': 'Return new access token'},
                      status.HTTP_401_UNAUTHORIZED: {'description': 'Refresh token is not valid or not provided'}
                  },
                  summary='Endpoint to obtain new access token, require valid refresh token')
async def get_access_token(token_data: Annotated[RefreshTokenData, Depends(require_refresh_token)],
                           query_mediator: Annotated[IQueryMediator, Depends(get_query_mediator)]):
    access_token_query = AccessTokenQuery(token_data.sub)
    response_schema = await query_mediator.execute_query(access_token_query)
    return response_schema

@user_router.get('/me',
                 status_code=status.HTTP_200_OK,
                 response_model=GetCurrentUserResponseSchema,
                 responses={
                     status.HTTP_200_OK: {'description': 'Return information about current authenticated user'},
                     status.HTTP_401_UNAUTHORIZED: {'description': 'User is not authenticated'},
                     status.HTTP_404_NOT_FOUND: {'description': 'User not found'}
                 },
                 summary='Endpoint to obtain information about current authenticated user')
async def get_current_user(user_id: Annotated[str, Depends(require_access_token)],
                           query_mediator: Annotated[IQueryMediator, Depends(get_query_mediator)]):
    get_current_user_query = GetCurrentUserQuery(user_id)
    try:
        response_schema = await query_mediator.execute_query(get_current_user_query)
    except LogicException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.message)
    else:
        return response_schema
    
@user_router.post('/logout',
                  status_code=status.HTTP_200_OK,
                  responses={
                      status.HTTP_200_OK: {'description': 'Logout success'},
                      status.HTTP_401_UNAUTHORIZED: {'description': 'User is not authenticated'}
                  },
                  summary='Endpoint for logout, revokes provided refresh token')
async def logout(token_data: Annotated[RefreshTokenData, Depends(require_refresh_token)],
                 command_mediator: Annotated[ICommandMediator, Depends(get_command_mediator)]):
    logout_command = LogoutCommand(jti=token_data.jti)
    try:
        await command_mediator.execute_command(logout_command)
    except AuthException as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ex.message)
