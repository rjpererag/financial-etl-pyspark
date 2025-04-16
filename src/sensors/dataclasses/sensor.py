from dataclasses import dataclass
from uuid import uuid4, UUID


@dataclass
class Sensor:
    id: str = str(uuid4())
    name: str = None
    active: bool = False
    type: str = None
    metric: str = None
    value: int | float = None


@dataclass
class SensorRead:
    metric: str = None
    value: int | float = None

