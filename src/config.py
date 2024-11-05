from pydantic import BaseModel, FilePath, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseModel):
    PREFIX: str


class PostgresSettings(BaseModel):
    URL: str


class AuthJWTSettings(BaseModel):
    PRIVATE_KEY_PATH: FilePath
    PUBLIC_KEY_PATH: FilePath
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: PositiveInt


class RedisSettings(BaseModel):
    URL: str
    TTL: PositiveInt


class Settings(BaseSettings):
    api: APISettings
    postgres: PostgresSettings
    auth: AuthJWTSettings
    redis: RedisSettings

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
