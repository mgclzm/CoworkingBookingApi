from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../../.env", env_file_encoding="utf-8")

    postgres_user: str = Field(alias="POSTGRES_USER", default="")
    postgres_password: str = Field(alias="POSTGRES_PASSWORD", default="")
    postgres_db: str = Field(alias="POSTGRES_DB", default="")
    postgres_host: str = Field(alias="POSTGRES_HOST", default="")
    postgres_port: str = Field(alias="POSTGRES_PORT", default="")

    @property
    def postgres_db_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    token_algorithm: str = Field(alias="TOKEN_ALGORITHM", default="")

    refresh_token_secret: str = Field(alias="REFRESH_TOKEN_SECRET", default="")
    refresh_token_lifetime: int = Field(alias="REFRESH_TOKEN_LIFETIME", default=0)

    access_token_secret: str = Field(alias="ACCESS_TOKEN_SECRET", default="")
    access_token_lifetime: int = Field(alias="ACCESS_TOKEN_LIFETIME", default=0)

    redis_host: str = Field(alias="REDIS_HOST", default="")
    redis_port: int = Field(alias="REDIS_PORT", default=0)
    redis_db: int = Field(alias="REDIS_DB", default=0)

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}"


settings = Settings()
