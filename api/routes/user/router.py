from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from domain.exceptions.errors import EmailAlreadyExistError
from api.app.dependecies import get_command_mediator
from api.routes.user.shemas import RegisterUserSchema
from logic.commands.user_commands import RegisterUserCommand
from logic.mediator.base import ICommandMediator

user_router = APIRouter(prefix='/v1', tags=['App user'])

@user_router.post('/user',
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