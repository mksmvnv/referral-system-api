from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_PREFIX: str

    DB_URL: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
