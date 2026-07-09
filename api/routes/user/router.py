from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from domain.exceptions.errors import EmailAlreadyExistError, InvalidUserCredentialsError, UserNotFoundError
from api.app.dependecies import get_command_mediator, get_query_mediator, require_refresh_token
from api.routes.user.shemas import AccessTokenResponseSchema, RefreshTokenResponseSchema, RegisterUserSchema
from logic.commands.user_commands import RegisterUserCommand
from logic.mediator.base import ICommandMediator, IQueryMediator
from logic.queries.user.user_queries import AccessTokenQuery, RefreshTokenQuery

user_router = APIRouter(prefix='/v1', tags=['App user'])

@user_router.post('/user/registration',
                  status_code=status.HTTP_201_CREATED,
                  responses={
                      status.HTTP_201_CREATED: {'description': 'User successfully registered'}, 
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
        await command_mediator.execute_command(register_user_command)
    except EmailAlreadyExistError as ex:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=ex.message) from ex

@user_router.post('/login', 
                  status_code=status.HTTP_200_OK, 
                  responses={
                      status.HTTP_200_OK: {'description': 'Return new refresh and access token pair'},
                      status.HTTP_401_UNAUTHORIZED: {'description': 'User is not registered, or the data provided is incorrect'}
                  },
                  response_model=RefreshTokenResponseSchema,
                  summary='Endpoint to obtain refresh token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                query_mediator: Annotated[IQueryMediator, Depends(get_query_mediator)]):
    refresh_token_query = RefreshTokenQuery(form_data.username, form_data.password)
    try:
        response_schema = await query_mediator.execute_query(refresh_token_query)
        return response_schema
    except (UserNotFoundError, InvalidUserCredentialsError) as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ex.message) from ex

@user_router.post('/access',
                  status_code=status.HTTP_200_OK,
                  response_model=AccessTokenResponseSchema,
                  responses={
                      status.HTTP_200_OK: {'description': 'Return new access token'},
                      status.HTTP_401_UNAUTHORIZED: {'description': 'Refresh token is not valid or not provided'}
                  },
                  summary='Entpoint to obtain new access token, require valid refresh token')
async def get_access_token(user_id: Annotated[str, Depends(require_refresh_token)],
                           query_mediator: Annotated[IQueryMediator, Depends(get_query_mediator)]):
    access_token_query = AccessTokenQuery(user_id)
    response_schema = await query_mediator.execute_query(access_token_query)
    return response_schema