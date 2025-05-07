# Realtime IoT Data Streaming - Kafka and Spark demonstration

## Project description
The goal of this project is to create a real world example on how we could deal with real time data
using Apache Kafka and Spark, as technologies to stream realtime data into a NoSQL database.

For the purpose of this project both Kafka and MongoDB will be launched using Docker using a docker-compose file, while
the remaining processes will be run in our local machine.

## Technologies
- Docker
- Apache Kafka
- Apache Spark
- MongoDB

## Structure
- IoT generator:
- Kafka Producer
- Spark Consumer

### IoT Generator:
This is our data generator simulating IoT metrics coming from home devices, for this demonstration we
will be simulating temperature and humidity metrics as inputs.

Other datapoints will be handled by this generator like device_id, room_id, etc. Simulating a real world
example involving IoT devices.

### Kafka Producer:
To stream data to our NoSQL DB we will leverage on Kafka in order to decouple and handle real-time streaming. With
this approach the producer we will handle sending the ingested data as JSON format (from our IoT simulator) and creating
the topic to which our consumer is going to consume from.

### Spark Consumer:
The final stage of this project is to consume the data from our Kafka topic, for this we will create a Spark consumer
by implementing a Kafka source (in this case the topic created before), to consume data from our queue, perform their
respective transformation, like Dataframe flattening, and write data to our target MongoDB collection.

## ENV Variables (Localhost example)

Note: The mongo credentials comes from our docker-compose file

- MONGO_URI=mongodb://root:example@localhost:27017
- MONGO_DATABASE=iot
- MONGO_COLLECTION=sensors_data
- MONGO_USER=root
- MONGO_PASSWORD=example