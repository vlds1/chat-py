from enum import Enum

from ariadne import EnumType


class Cities(Enum):
    MOSCOW = "Moscow"
    ROSTOV_ON_DON = "Rostov-on-Don"
    BERLIN = "Berlin"
    WASHINGTON = "Washington"
    KIEV = "Kyiv"
    MINSK = "Minsk"
    PARIS = "Paris"


cities = EnumType("Cities", Cities)
