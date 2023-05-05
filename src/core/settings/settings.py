from functools import lru_cache
import typing
from pydantic import BaseSettings
from pydantic import Field
from uvicorn.config import (
    HTTPProtocolType,
    LoopSetupType,
)

from src.core.settings.base import _BaseModel


class SqlAlchemySettings(_BaseModel):
    """SQLAlchemy settings"""

    url: str = None


class UvicornSettings(_BaseModel):
    """Uvicorn Settings"""

    app: str = "main:app"
    host: str = "0.0.0.0"
    port: int = 8000
    loop: LoopSetupType = "auto"
    http: HTTPProtocolType = "auto"
    reload: bool = Field(default=None, description="Enable auto-reload.")
    workers: int | None = None


class DatabaseSettings(_BaseModel):
    """Database Settings"""

    echo: bool = False

    url: typing.Any

    pool_size: int = 1
    max_overflow: int = 5
    pool_timeout: int = 30
    pool_recycle: int = -1
    pool_pre_ping: bool = False


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

    kafka_topic: str
    kafka_bootstrap_servers: str
    kafka_consumer_group: str

    redis_url: str


@lru_cache
def get_settings() -> Settings:
    """Получение и кэширование настроек проекта."""
    _settings = Settings()
    return _settings


settings = get_settings()