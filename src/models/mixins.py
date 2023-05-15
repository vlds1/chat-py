from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class TimingMixin:
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Время создания записи"
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="Время последнего обновления записи"
    )
