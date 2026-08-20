import json

from kafka import KafkaConsumer


TOPIC = "stream-events"
BOOTSTRAP_SERVER = "localhost:9092"


consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVER,
    group_id="stream-forge-consumer",
    auto_offset_reset="earliest",
    value_deserializer=lambda value: json.loads(
        value.decode("utf-8")
    )
)


print("=" * 60)
print("       STREAM FORGE - KAFKA TELEMETRY CONSUMER")
print("=" * 60)
print(f"Topic: {TOPIC}")
print("Waiting for truck telemetry...\n")


try:
    for message in consumer:
        event = message.value

        print("Received Telemetry")
        print("-" * 40)

        print(f"Truck ID     : {event.get('truck_id')}")
        print(f"Temperature  : {event.get('temperature')} °C")
        print(f"Timestamp    : {event.get('timestamp')}")

        print(f"Topic        : {message.topic}")
        print(f"Partition    : {message.partition}")
        print(f"Offset       : {message.offset}")

        print("-" * 40)

except KeyboardInterrupt:
    print("\nConsumer stopped by user.")

finally:
    consumer.close()
    print("Kafka consumer closed.")
