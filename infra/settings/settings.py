from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../../.env', env_file_encoding='utf-8')

    postgres_user: str = Field(alias='POSTGRES_USER')
    postgres_password: str = Field(alias='POSTGRES_PASSWORD')
    postgres_db: str = Field(alias='POSTGRES_DB')
    postgres_host: str = Field(alias='POSTGRES_HOST')
    postgres_port: str = Field(alias='POSTGRES_PORT')

    @property
    def postgres_db_url(self) -> str:
        return f'postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'
    