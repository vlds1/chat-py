from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class WeatherRequest(_message.Message):
    __slots__ = ["city"]
    CITY_FIELD_NUMBER: _ClassVar[int]
    city: str
    def __init__(self, city: _Optional[str] = ...) -> None: ...

class WeatherResponse(_message.Message):
    __slots__ = ["weather"]
    WEATHER_FIELD_NUMBER: _ClassVar[int]
    weather: str
    def __init__(self, weather: _Optional[str] = ...) -> None: ...
