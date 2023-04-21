from decimal import Decimal

from pydantic import BaseModel


class Message(BaseModel):
    message: str


class WeatherSchema(BaseModel):
    class Config:
        orm_mode = True

    city: str
    current_temperature: Decimal
    current_weather: str
    current_wind_speed: Decimal
    current_humidity: int
    sunrise: str
    sunset: str
    day_duration: str
