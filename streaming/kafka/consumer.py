import json
from kafka import KafkaConsumer

TOPIC = "stream-events"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers="localhost:9092",
    group_id="stream-forge-consumer",
    auto_offset_reset="earliest",
    value_deserializer=lambda value: json.loads(
        value.decode("utf-8")
    )
)

print("=" * 50)
print("        STREAM FORGE - KAFKA CONSUMER")
print("=" * 50)
print(f"Topic: {TOPIC}")
print("Waiting for messages...\n")
