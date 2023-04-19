from sqlalchemy import (
    Column,
    String,
    Integer,
)
from models.base_class import Base


class WeatherData(Base):
    __tablename__ = "weather"
    __table_args__ = {"comment": "Данные о погоде"}

    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )

    city = Column(
        String(20),
        primary_key=False,
        nullable=False,
        unique=True,
        default=0,
    )
