from pydantic.networks import MultiHostDsn
from src.core.settings.base import _BaseModel


class SqlAlchemySettings(_BaseModel):
    """SQLAlchemy settings"""

    url: str = None
