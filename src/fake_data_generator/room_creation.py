from src.sensors.dataclasses.sensor import Sensor
from src.sensors.dataclasses.room import Room


def create_room() -> Room:
    my_sensors = [
        Sensor(
            name="my_temperature",
            active=True,
            type="temperature",
        ),
        Sensor(
            name="my_humidity",
            active=True,
            type="humidity"
        )
    ]

    return Room(
        name="living room",
        sensors=my_sensors
    )
