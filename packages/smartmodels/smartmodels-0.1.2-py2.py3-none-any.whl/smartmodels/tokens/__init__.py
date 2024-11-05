# tokens
# TODO: split into several files as the number of tokens grow

from enum import Enum


class StrEnum(str, Enum):
    """Enum where members are also (and must be) str"""


class NAMESPACES(StrEnum):
    CONFORT = "confort"
    CONSUMPTION = "consumption"
    ENERGY = "energy"
    RADIATION = "radiation"  # is a TYPE?
    TRACKING = "tracking"
    TRAFFIC = "traffic"
    WARNINGS = "warning"
    WASTE = "waste"
    WATERING = "watering"  # is a TYPE?
    WEATHER = "weather"


class TYPES(StrEnum):
    AIR = "air"
    CONTAINER = "container"
    ELECTRICITY = "electricity"
    ELECTROMAGNETIC = "electromagnetic"
    FLOOD = "flood"
    HEARTQUAKE = "heartquake"
    NOISE = "noise"
    OCCUPANCY = "occupancy"
    PERSON = "person"
    STRUCTURE = "structure"
    WATER = "water"
    XYLOPHAGES = "xylophages"


class LOCATION(StrEnum):
    ALL = "all"
    BUILDING = "building"
    INDOOR = "indoor"
    OUTDOOR = "outdoor"
    PARKING = "parking"


class ASPECT(StrEnum):
    QUALITY = "quality"
