from ..dataclasses.room import Room
from ..dataclasses.sensor import SensorRead, Sensor
import random


class RoomDataGenerator:

    def __init__(self, room: Room):
        self.room = room

    @staticmethod
    def __random_increment(value: int | float, min_: float, max_: float) -> float:
        increment = random.uniform(min_, max_)
        return value*(1+increment)

    def _generate_humidity(self) -> float:
        return self.__random_increment(value=10, min_=0.10, max_=0.20)

    def _generate_temperature(self) -> float:
        return self.__random_increment(value=20, min_=0.05, max_=0.10)

    def generate_sensor_data(self, sensor: Sensor) -> SensorRead | None:
        read = SensorRead()
        if sensor.active:
            if sensor.type == "temperature":
                read.metric = "Cª"
                read.value = self._generate_temperature()

            elif sensor.type == "humidity":
                read.metric = "%"
                read.value = self._generate_humidity()

        return read

    def generate_room_data(self) -> Room:
        if self.room and self.room.sensors:
            print(f"Reading sensors from: {self.room.name}: {self.room.id}")  # TODO: Log
            for sensor in self.room.sensors:
                print(f"    Reading sensor {sensor.name}: {sensor.id}")  # TODO: LOG
                if read := self.generate_sensor_data(sensor=sensor):
                    print(f"        Sensor {sensor.name}: {sensor.id} successfully read")
                    sensor.value = read.value
                    sensor.metric = read.metric

        return self.room
