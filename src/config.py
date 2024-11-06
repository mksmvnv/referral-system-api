from pathlib import Path
from pydantic import BaseModel, FilePath, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseModel):
    PREFIX: str = "/api"


class PostgresSettings(BaseModel):
    URL: str = "postgresql://user:password@localhost/dbname"


class AuthJWTSettings(BaseModel):
    PRIVATE_KEY_PATH: FilePath = Path("path/to/private.key")
    PUBLIC_KEY_PATH: FilePath = Path("path/to/public.key")
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: PositiveInt = 15


class RedisSettings(BaseModel):
    URL: str = "redis://localhost:6379"
    TTL: PositiveInt = 300


class Settings(BaseSettings):
    api: APISettings = APISettings()
    postgres: PostgresSettings = PostgresSettings()
    auth: AuthJWTSettings = AuthJWTSettings()
    redis: RedisSettings = RedisSettings()

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
