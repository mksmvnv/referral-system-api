from pydantic import BaseModel, FilePath, StrictStr, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseModel):
    prefix: StrictStr


class PostgresSettings(BaseModel):
    url: StrictStr


class AuthJWTSettings(BaseModel):
    private_key_path: FilePath
    public_key_path: FilePath
    algorithm: StrictStr
    access_token_expire_minutes: PositiveInt


class RedisSettings(BaseModel):
    url: StrictStr
    ttl: PositiveInt


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
