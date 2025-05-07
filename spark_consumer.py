from spark_consumer import create_spark_settings, SparkConsumer


def main() -> None:
    settings = create_spark_settings()
    consumer = SparkConsumer(settings=settings)
    consumer.consume()


if __name__ == "__main__":
    main()
