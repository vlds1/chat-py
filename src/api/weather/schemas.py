from pydantic import BaseModel
from pydantic import PositiveFloat


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
