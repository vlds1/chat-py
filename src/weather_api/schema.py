from pydantic import BaseModel
from pydantic import PositiveFloat


class Message(BaseModel):
    message: str


class WeatherSchema(BaseModel):
    class Config:
        orm_mode = True

    city: str
    current_temperature: PositiveFloat
    current_weather: str
    current_wind_speed: PositiveFloat
    current_humidity: int
    sunrise: str
    sunset: str
    day_duration: str
    reqeust_time: str
