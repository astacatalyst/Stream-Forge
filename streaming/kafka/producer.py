mport json
import time
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

TOPIC = "stream-events"

events = [
    {
        "id": 1,
        "name": "Gaming Live",
        "status": "active"
    },
    {
        "id": 2,
        "name": "Payment Stream",
        "status": "active"
    },
    {
        "id": 3,
        "name": "Order Stream",
        "status": "active"
    }
]

for event in events:
    producer.send(TOPIC, value=event)
    print(f"Sent: {event}")
    time.sleep(1)

producer.flush()
producer.close()