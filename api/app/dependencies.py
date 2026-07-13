import jwt
import punq

from typing import Annotated, Optional, cast

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer

from api.app.container import init_container, typed_resolve
from api.routes.user.security import AuthError, CompositeRefreshTokenValidator, RefreshTokenClaimsValidator, RefreshTokenData, RefreshTokenJtiValidator, RefreshTokenTypeValidator, TokenType
from logic.mediator.base import ICommandMediator, IQueryMediator
from infra.settings.settings import settings
from logic.uow.base import BaseUnitOfWork

def get_command_mediator() -> ICommandMediator:
    container = init_container()
    return typed_resolve(container, ICommandMediator)

def get_query_mediator() -> IQueryMediator:
    container = init_container()
    return typed_resolve(container, IQueryMediator)

refresh_oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login', auto_error=False)
access_oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/access', auto_error=False, refreshUrl='login')

async def require_refresh_token(refresh_token: Annotated[Optional[str], Security(refresh_oauth2_scheme)],
                          container: Annotated[punq.Container, Depends(init_container)]) -> RefreshTokenData:
    if refresh_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Refresh token is not provided')
    
    try:
        payload = jwt.decode(refresh_token, settings.refresh_token_secret, algorithms=[settings.token_algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Provided token is expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')
    
    refresh_token_validator = CompositeRefreshTokenValidator(
        required_claims_validator=RefreshTokenClaimsValidator(),
        validators=[RefreshTokenTypeValidator(), RefreshTokenJtiValidator(typed_resolve(container, BaseUnitOfWork))]
    )
    try:
        await refresh_token_validator.validate(payload)
    except AuthError as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ex.message) from ex
    
    user_id = cast(str, payload.get('sub'))
    jti = cast(str, payload.get('jti'))
    return RefreshTokenData(sub=user_id, jti=jti)

def require_access_token(access_token: Annotated[Optional[str], Security(access_oauth2_scheme)]) -> str:
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Access token is not provided')
    
    try:
        payload = jwt.decode(access_token, settings.acess_token_secret, algorithms=[settings.token_algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Provided token is expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid access token')
    
    token_type = cast(TokenType, payload.get('type'))
    if token_type != TokenType.ACCESS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token type is not "access"')
    
    user_id = cast(str, payload.get('sub'))
    return user_id
