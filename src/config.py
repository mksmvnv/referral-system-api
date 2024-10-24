from pydantic import PositiveInt
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_prefix: str
    postgres_url: str
    referral_code_expiry: PositiveInt

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
