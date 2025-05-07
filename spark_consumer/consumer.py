from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import col, from_json, explode

from .settings import SparkConsumerSettings


class SparkConsumer:

    def __init__(self, settings: SparkConsumerSettings):
        self.settings = settings

        spark_config = settings.spark_session

        self.spark = SparkSession \
            .builder \
            . appName(spark_config.app_name) \
            .master(spark_config.master) \
            .config("spark.mongodb.output.uri", settings.mongo.uri) \
            .config("spark.jars.packages", spark_config.packages) \
            .getOrCreate()

        self.spark.sparkContext.setLogLevel("WARN")

    def read_stream(self) -> DataFrame:
        return self.spark.readStream \
            .format(source="kafka") \
            .option(key="kafka.bootstrap.servers", value=self.settings.bootstrap_servers) \
            .option(key="subscribe", value=self.settings.kafka_topic) \
            .option(key="startingOffsets", value=self.settings.starting_offsets) \
            .option(key="failOnDataLoss", value=self.settings.fail_on_data_loss) \
            .load()

    def _write_to_mongo(self, df: DataFrame) -> None:
        df.write.format("mongo") \
            .option("uri", self.settings.mongo.uri) \
            .option("database", self.settings.mongo.database) \
            .option("collection", self.settings.mongo.collection) \
            .mode("append") \
            .save()

    def write_to_mongo(self, df: DataFrame):
        df_sensors = df.select("data.name", "data.id", explode("data.sensors").alias("sensors"))
        df_to_send = df_sensors.select(
            col("name").alias("device_name"),
            col("id").alias("device_id"),
            "sensors.id",
            "sensors.name",
            "sensors.active",
            "sensors.type",
            "sensors.metric",
            "sensors.value",
        )

        df_to_send.show()

        self._write_to_mongo(df=df_to_send)

    def consume(self) -> None:  # TODO REVIEW
        df_raw = self.read_stream()
        df_parsed = df_raw.selectExpr("CAST(value AS STRING) as json_string")
        df_json = df_parsed.select(
            from_json(col("json_string"), self.settings.schemas.message_schema).alias("data"))

        df_sensors = df_json.select(
            col("data.name").alias("device_name"),
            col("data.id").alias("device_id"),
            explode(col("data.sensors")).alias("sensor")
        )

        df_to_send = df_sensors.select(
            "device_name",
            "device_id",
            col("sensor.id").alias("sensor_id"),
            col("sensor.name").alias("sensor_name"),
            col("sensor.active").alias("sensor_active"),
            col("sensor.type").alias("sensor_type"),
            col("sensor.metric").alias("sensor_metric"),
            col("sensor.value").alias("sensor_value"),
        )

        def write_to_mongodb(df, epoch_id):
            df.write.format("mongo") \
                .option("uri", self.settings.mongo.uri) \
                .option("database", self.settings.mongo.database) \
                .option("collection", self.settings.mongo.collection) \
                .mode("append") \
                .save()

        query = df_to_send.writeStream \
            .foreachBatch(write_to_mongodb) \
            .outputMode("append") \
            .option("checkpointLocation", self.settings.checkpoint_location) \
            .start()

        query.awaitTermination()

