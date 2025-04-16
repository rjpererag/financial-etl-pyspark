from dataclasses import dataclass, field
from uuid import uuid4, UUID
from .sensor import Sensor


@dataclass
class Room:
    name: str = None
    id: str = str(uuid4())
    sensors: list[Sensor] = field(default_factory=list)
