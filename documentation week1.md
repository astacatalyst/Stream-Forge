
# Stream-Forge - Week 1 Documentation

## Kafka Setup
- Set up a local Apache Kafka environment using Docker.
- Connected the Python Kafka applications to the Kafka broker through `localhost:9092`.
- Used the Kafka topic `stream-events`.

## Kafka Producer
- Created `producer.py` inside the `streaming` folder.
- Configured a Kafka producer using `KafkaProducer`.
- Configured JSON serialization for the event messages.
- Sent mock streaming events to the `stream-events` topic.
- The events contain:
  - `id`
  - `name`
  - `status`
- Added a short delay between messages and flushed the producer after sending the events.

## Kafka Consumer
- Created `consumer.py` inside the `streaming` folder.
- Configured a Kafka consumer using `KafkaConsumer`.
- Connected the consumer to the `stream-events` topic.
- Used the consumer group `stream-forge-consumer`.
- Configured `auto_offset_reset` as `earliest`.
- Configured JSON deserialization to convert Kafka messages back into Python objects.
- Displayed the received event details along with the topic, partition, and offset.

## Testing
- Ran the Kafka consumer and producer in separate VS Code terminals.
- Verified that the producer successfully sent events to Kafka.
- Verified that the consumer successfully received and displayed the events.
- Successfully tested the complete flow:

`Producer → Kafka Topic → Consumer`

## Week 1 Status
- Kafka producer and consumer communication tested successfully.
- Messages were successfully produced and consumed through Kafka.
