from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

class RegisterUserSchema(BaseModel):
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=3, max_length=255)

class RegisterUserResponseSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    user_id: str
    created_at: datetime

class IssueRefreshTokenResponseSchema(BaseModel):
    refresh_token: str
    access_token: str

class AccessTokenResponseSchema(BaseModel):
    token_type: str
    access_token: str

class GetCurrentUserResponseSchema(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: str
