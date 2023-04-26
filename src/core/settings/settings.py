from functools import lru_cache
from pydantic import Field
from uvicorn.config import (
    HTTPProtocolType,
    LoopSetupType,
)
from src.core.settings.base import _BaseModel
from pydantic import BaseSettings


class UvicornSettings(_BaseModel):
    """Uvicorn Settings"""

    app: str = "main:app"
    host: str = "0.0.0.0"
    port: int = 8001
    loop: LoopSetupType = "uvloop"
    http: HTTPProtocolType = "auto"
    reload: bool = Field(default=None, description="Enable auto-reload.")
    workers: int | None = None


class Settings(BaseSettings):
    """Service API settings."""

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"

    api_prefix: str = ""
    root_path: str = ""
    app_version: str = "latest"

    project_name: str = "weather-collector"
    app_slug: str = ""

    debug: bool | None

    kafka_topic: str
    kafka_bootstrap_servers: str
    kafka_consumer_group: str
    open_weather_token: str

    uvicorn: UvicornSettings = UvicornSettings()


@lru_cache
def get_settings() -> Settings:
    """Получение и кэширование настроек проекта."""
    _settings = Settings()
    return _settings


settings = get_settings()
