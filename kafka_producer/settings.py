from dataclasses import dataclass


@dataclass
class KafkaSettings:
    bootstrap_servers: str = None
    topic: str = None
    sleep_time: int = 1


def create_kafka_settings() -> KafkaSettings:
    return KafkaSettings(
        bootstrap_servers="localhost:9092",
        topic="iot_data",
        sleep_time=10
    )
