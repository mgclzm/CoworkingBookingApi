from pydantic import BaseModel, Field, EmailStr

class RegisterUserSchema(BaseModel):
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=3, max_length=255)

class RefreshTokenResponseSchema(BaseModel):
    refresh_token: str
    access_token: str

class AccessTokenResponseSchema(BaseModel):
    token_type: str
    access_token: str