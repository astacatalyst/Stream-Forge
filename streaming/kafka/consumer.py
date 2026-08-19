import json
from kafka import KafkaConsumer

TOPIC = "stream-events"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset="latest",
    enable_auto_commit=True,
    group_id="truck-consumer-group"
)

print("Consumer started...")

for message in consumer:
    data = message.value

    print(
        f"Truck ID: {data['truck_id']} | "
        f"Location: {data['location']} | "
        f"Speed: {data['speed']} km/h | "
        f"Fuel: {data['fuel']}%"
    )