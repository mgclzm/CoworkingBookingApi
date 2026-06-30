from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../../.env', env_file_encoding='utf-8')

    postgres_user: str = Field(alias='POSTGRES_USER', default='')
    postgres_password: str = Field(alias='POSTGRES_PASSWORD', default='')
    postgres_db: str = Field(alias='POSTGRES_DB', default='')
    postgres_host: str = Field(alias='POSTGRES_HOST', default='')
    postgres_port: str = Field(alias='POSTGRES_PORT', default='')

    @computed_field
    @property
    def postgres_db_url(self) -> str:
        return f'postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'
    
settings = Settings() 