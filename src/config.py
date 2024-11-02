from pydantic import BaseModel, FilePath, StrictStr, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseModel):
    PREFIX: StrictStr


class PostgresSettings(BaseModel):
    URL: StrictStr


class AuthJWTSettings(BaseModel):
    PRIVATE_KEY_PATH: FilePath
    PUBLIC_KEY_PATH: FilePath
    ALGORITHM: StrictStr
    ACCESS_TOKEN_EXPIRE_MINUTES: PositiveInt


class RedisSettings(BaseModel):
    URL: StrictStr
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
