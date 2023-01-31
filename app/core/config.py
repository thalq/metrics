from pydantic import BaseSettings


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
