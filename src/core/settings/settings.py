from functools import lru_cache

from pydantic import BaseSettings

from src.core.settings.database import DatabaseSettings
from src.core.settings.sqlalchemy import SqlAlchemySettings
from src.core.settings.uvicorn import UvicornSettings


class Settings(BaseSettings):
    """Service API settings."""

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"

    api_prefix: str = ""
    root_path: str = ""
    app_version: str = "latest"

    project_name: str
    app_slug: str

    debug: bool | None

    postgres: DatabaseSettings = DatabaseSettings()
    uvicorn: UvicornSettings = UvicornSettings()
    sqlalchemy: SqlAlchemySettings = SqlAlchemySettings()


@lru_cache
def get_settings() -> Settings:
    """Получение и кэширование настроек проекта."""
    _settings = Settings()
    return _settings


settings = get_settings()