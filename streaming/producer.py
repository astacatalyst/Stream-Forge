import json
import random
import time
from datetime import datetime, timezone

from kafka import KafkaProducer


TOPIC = "stream-events"
BOOTSTRAP_SERVER = "localhost:9092"


producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVER,
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)


print("=" * 60)
print("       STREAM FORGE - KAFKA TELEMETRY PRODUCER")
print("=" * 60)
print(f"Topic: {TOPIC}")
print("Generating real-time mock truck telemetry...\n")


try:
    while True:

        # Generate mock truck telemetry
        event = {
            "truck_id": f"TRUCK-{random.randint(1001, 1050)}",
            "temperature": round(random.uniform(20.0, 40.0), 2),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        # Send telemetry to Kafka
        producer.send(TOPIC, value=event)

        print(f"Sent: {event}")

        # Generate a new event every second
        time.sleep(1)

except KeyboardInterrupt:
    print("\nProducer stopped by user.")

finally:
    producer.flush()
    producer.close()
    print("Kafka Producer closed.")