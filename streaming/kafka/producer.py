import time
import random
import json
from datetime import datetime
from kafka import KafkaProducer


# ---------------- KAFKA PRODUCER ----------------

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

TOPIC = "truck-data"


# ---------------- TRUCK DATA ----------------

trucks = [
    {
        "truck_id": "T101",
        "location": "Nagpur",
        "speed": 45,
        "fuel": 78,
        "temperature": 28
    },
    {
        "truck_id": "T102",
        "location": "Wardha",
        "speed": 52,
        "fuel": 64,
        "temperature": 30
    },
    {
        "truck_id": "T103",
        "location": "Bhandara",
        "speed": 38,
        "fuel": 81,
        "temperature": 27
    },
    {
        "truck_id": "T104",
        "location": "Amravati",
        "speed": 50,
        "fuel": 70,
        "temperature": 29
    },
    {
        "truck_id": "T105",
        "location": "Akola",
        "speed": 42,
        "fuel": 75,
        "temperature": 31
    }
]


print("=" * 75)
print("           🚚 REAL-TIME TRUCK MONITORING SYSTEM")
print("=" * 75)
print(f"Kafka Topic : {TOPIC}")
print("Status      : PRODUCER RUNNING")
print("Update Rate : Every 2 seconds")
print("=" * 75)


# ---------------- CONTINUOUS STREAM ----------------

while True:

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n🕐 UPDATE TIME: {timestamp}")
    print("-" * 75)

    for truck in trucks:

        # Dynamic speed
        truck["speed"] += random.randint(-4, 4)
        truck["speed"] = max(20, min(80, truck["speed"]))

        # Dynamic fuel
        truck["fuel"] -= random.choice([0, 0, 1])
        truck["fuel"] = max(0, truck["fuel"])

        # Dynamic temperature
        truck["temperature"] += random.choice([-1, 0, 0, 1])
        truck["temperature"] = max(20, min(40, truck["temperature"]))

        # Determine truck status
        if truck["fuel"] <= 20:
            status = "LOW_FUEL"
        elif truck["speed"] < 25:
            status = "IDLE"
        else:
            status = "ON_ROUTE"

        # Create message
        data = {
            "truck_id": truck["truck_id"],
            "location": truck["location"],
            "speed": truck["speed"],
            "fuel": truck["fuel"],
            "temperature": truck["temperature"],
            "status": status,
            "timestamp": timestamp
        }

        # Send to Kafka
        producer.send(TOPIC, value=data)

        # Display
        print(
            f"🚚 {data['truck_id']} | "
            f"📍 {data['location']:<10} | "
            f"⚡ {data['speed']:>2} km/h | "
            f"⛽ {data['fuel']:>2}% | "
            f"🌡️ {data['temperature']}°C | "
            f"{data['status']}"
        )

    producer.flush()

    print("-" * 75)
    print("✅ 5 truck records sent successfully")
    print("⏳ Waiting 2 seconds for next update...")

    time.sleep(2)