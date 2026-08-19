import json
import json
import time
from datetime import datetime, timezone

from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

TOPIC = "stream-events"

events = [
    {
        "truck_id": "TRUCK001",
        "temperature": 25.5
    },
    {
        "truck_id": "TRUCK002",
        "temperature": 27.2
    },
    {
        "truck_id": "TRUCK003",
        "temperature": 24.8
    }
]

for event in events:
    event["timestamp"] = datetime.now(timezone.utc).isoformat()

    producer.send(TOPIC, value=event)
    print(f"Sent: {event}")
    time.sleep(1)

    producer.flush()

    print("-" * 75)
    print("✅ 5 truck records sent successfully")
    print("⏳ Waiting 2 seconds for next update...")

    time.sleep(2)