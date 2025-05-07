from kafka_producer import create_kafka_settings, KafkaSensorsProducer


def main() -> None:
    settings = create_kafka_settings()
    producer = KafkaSensorsProducer(settings=settings)
    producer.produce()


if __name__ == "__main__":
    main()
