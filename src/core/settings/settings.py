from pydantic import BaseSettings
from pydantic import Field
from uvicorn.config import HTTPProtocolType
from uvicorn.config import LoopSetupType

from src.core.settings.base import _BaseModel


class UvicornSettings(_BaseModel):
    """Uvicorn Settings"""

    app: str = "main:app"
    host: str = "0.0.0.0"
    port: int = 8000
    loop: LoopSetupType = "auto"
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

    project_name: str
    app_slug: str

    debug: bool | None

    uvicorn: UvicornSettings = UvicornSettings()

    kafka_topic: str
    kafka_bootstrap_servers: str
    kafka_consumer_group: str

    redis_url: str
    redis_ttl: int = 10
    graphql_url: str


def get_settings() -> Settings:
    """Получение и кэширование настроек проекта."""
    _settings = Settings()
    return _settings


settings = get_settings()