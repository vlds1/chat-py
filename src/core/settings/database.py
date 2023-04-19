import typing

from src.core.settings.base import _BaseModel


class DatabaseSettings(_BaseModel):
    """Database Settings"""

    echo: bool = False

    url: typing.Any

    pool_size: int = 1
    max_overflow: int = 5
    pool_timeout: int = 30
    pool_recycle: int = -1
    pool_pre_ping: bool = False
