from src.sensors.service.generator import RoomDataGenerator
from dataclasses import asdict


def generate_data(room_data_generator: RoomDataGenerator) -> dict:
    room_data = room_data_generator.generate_room_data()
    return asdict(room_data)
