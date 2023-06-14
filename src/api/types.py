from enum import Enum

from pydantic import BaseModel, PositiveFloat

from ariadne import EnumType


class Cities(Enum):
    MOSCOW = "Moscow"
    ROSTOV_ON_DON = "Rostov-on-Don"
    BERLIN = "Berlin"
    WASHINGTON = "Washington"
    KIEV = "Kyiv"
    MINSK = "Minsk"
    PARIS = "Paris"


class WeatherSchema(BaseModel):
    city: str
    current_temperature: PositiveFloat
    current_weather: str
    current_wind_speed: PositiveFloat
    current_humidity: int
    sunrise: str
    sunset: str
    day_duration: str
    request_time: str

cities = EnumType("Cities", Cities)
