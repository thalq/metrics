import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL").format(
    POSTGRES_USER=os.getenv("POSTGRES_USER"),
    POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD"),
    POSTGRES_HOST=os.getenv("POSTGRES_HOST"),
    POSTGRES_PORT=os.getenv("POSTGRES_PORT"),
    POSTGRES_DB=os.getenv("POSTGRES_DB"),
)


class Settings(BaseSettings):
    app_title: str = "Рассчет метрики"
    database_url: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_port: str

    class Config:
        env_file = ".env"


settings = Settings()
settings.database_url = DATABASE_URL
