import json
import time

from kafka import KafkaProducer

from src.fake_data_generator.generator import generate_data
from src.fake_data_generator.room_creation import create_room
from src.sensors.service.generator import RoomDataGenerator

from .settings import KafkaSettings


class KafkaSensorsProducer:

    def __init__(self, settings: KafkaSettings):
        self.settings = settings

    def __create_producer(self) -> KafkaProducer:
        return KafkaProducer(
            bootstrap_servers=self.settings.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def produce(self):
        producer = self.__create_producer()
        room = create_room()
        room_data_generator = RoomDataGenerator(room=room)

        while True:
            data = generate_data(room_data_generator=room_data_generator)
            producer.send(topic=self.settings.topic, value=data)
            time.sleep(self.settings.sleep_time)
