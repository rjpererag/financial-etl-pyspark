from decouple import config
from dataclasses import dataclass, field
from pyspark.sql.types import StructType, StructField, StringType, BooleanType, DoubleType, ArrayType


@dataclass
class Schemas:
    sensor_schema: StructType = field(default_factory=StructType)
    message_schema: StructType = field(default_factory=StructType)


@dataclass
class MongoConfig:
    user: str = None
    password: str = None
    uri: str = None
    database: str = None
    collection: str = None


@dataclass
class SparkSessionConfig:
    app_name: str = None
    master: str = None
    packages: str = None


@dataclass
class SparkConsumerSettings:
    spark_session: SparkSessionConfig = SparkSessionConfig()
    mongo: MongoConfig = MongoConfig()
    schemas: Schemas = Schemas()
    bootstrap_servers: str = None
    kafka_topic: str = None
    starting_offsets: str = None
    checkpoint_location: str = None
    fail_on_data_loss: str = None


def create_spark_settings() -> SparkConsumerSettings:
    # SPARK SESSION
    spark_session = SparkSessionConfig(
        app_name="iot_kafka_stream_reader",
        master="local[*]",
        packages="org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1"
    )

    # MONGO DB
    mongo = MongoConfig(
        uri=config("MONGO_URI"),
        user=config("MONGO_USER"),
        password=config("MONGO_PASSWORD"),
        database=config("MONGO_DATABASE"),
        collection=config("MONGO_COLLECTION")
    )

    # SCHEMAS SETTINGS
    sensor_schema = StructType([
        StructField("id", StringType(), True),
        StructField("name", StringType(), True),
        StructField("active", BooleanType(), True),
        StructField("type", StringType(), True),
        StructField("metric", StringType(), True),
        StructField("value", DoubleType(), True),
    ])

    message_schema = StructType([
        StructField("name", StringType(), True),
        StructField("id", StringType(), True),
        StructField("sensors", ArrayType(sensor_schema), True)
    ])

    schemas = Schemas(
        sensor_schema=sensor_schema,
        message_schema=message_schema
    )

    # SPARK CONSUMER SETTINGS
    spark_consumer_settings = SparkConsumerSettings(
        spark_session=spark_session,
        mongo=mongo,
        schemas=schemas,
        bootstrap_servers="localhost:9092",
        kafka_topic="iot_data",
        starting_offsets="latest",
        checkpoint_location="/tmp/spark-checkpoints/transactions-stream",
        fail_on_data_loss="false"
    )

    return spark_consumer_settings
