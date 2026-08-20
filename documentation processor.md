1. Week 2 Objective

The main objective of Week 2 was to implement the real-time stream processing layer of the Stream Forge project using Faust.

The Kafka producer developed earlier generates continuous truck telemetry data and publishes it to the Kafka topic stream-events. In Week 2, a Faust-based stream processor was developed to consume these events from Kafka and process them in real time.

2. Technologies Used

Technology	    Purpose
Python 3.11.9	Programming environment
Apache Kafka	Real-time event/message streaming
Faust 0.13.2	Stream processing framework
aiokafka 0.14.0	Kafka transport used by Faust
Docker	Running the Kafka broker
VS Code	Development environment
3. System Architecture


The Week 2 processing architecture is:

┌──────────────────────┐
│   Kafka Producer     │
│     producer.py      │
└──────────┬───────────┘
           │
           │ Truck Telemetry
           ▼
┌──────────────────────┐
│    Kafka Broker      │
│   localhost:9092     │
└──────────┬───────────┘
           │
           │ stream-events
           ▼
┌──────────────────────┐
│   Faust Processor    │
│ stream_processor.py  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Processed Events    │
│ Truck Telemetry Data  │
└──────────────────────┘

4. Project File Structure

During Week 2, the streaming-related structure was:

Stream-Forge
│
├── streaming
│   ├── stream_processor.py
│   │
│   └── kafka
│       ├── producer.py
│       ├── consumer.py
│       └── database.py

The main file developed for Week 2 was:

streaming/stream_processor.py

5. Faust Application Configuration

A Faust application named:

stream-forge-processor

was configured to connect to Kafka using:

kafka://localhost:9092

The application uses an in-memory store for the current processing implementation.

The Kafka topic used for telemetry events is:

stream-events


6. Event Data Structure

The processor handles truck telemetry containing three primary fields:

truck_id
temperature
timestamp

Example event:

{
    "truck_id": "TRUCK-1036",
    "temperature": 31.4,
    "timestamp": "2026-08-20T09:44:12.016558+00:00"
}
Field Description
Field	Description
truck_id	Unique identifier of the truck
temperature	Current truck temperature reading
timestamp	Time at which the telemetry event was generated


7. Stream Processor Implementation

A Faust record was created to represent the incoming telemetry event.

The Kafka topic stream-events was configured with the telemetry record as its value type.

A Faust agent was then implemented to continuously consume events from the Kafka topic.

The processor performs the following operations:

Connects to the Kafka broker.
Subscribes to the stream-events topic.
Receives truck telemetry events.
Deserializes the event data.
Processes each event using the Faust agent.
Displays the processed truck information.

8. Running the Stream Processor

The processor was executed using Python 3.11:

py -3.11 streaming\stream_processor.py worker

Faust successfully started with the following configuration:

Faust version: 0.13.2
Application: stream-forge-processor
Broker: kafka://localhost:9092
Platform: CPython 3.11.9

9. Producer Execution

The existing Kafka producer was executed using:

py -3.11 streaming\kafka\producer.py

The producer continuously generated mock truck telemetry and sent it to the Kafka topic.

Example:

Sent: {
    'truck_id': 'TRUCK-1017',
    'temperature': 29.4,
    'timestamp': '2026-08-20T09:47:15.456598+00:00'
}

The producer generates a new telemetry event approximately every second.

10. Stream Processing Output

The Faust processor successfully consumed and processed the Kafka events.

Example output:

Processed Event -> Truck: TRUCK-1033,
Temperature: 37.51°C,
Timestamp: 2026-08-20T09:46:40.381447+00:00

Additional events were continuously processed:

Processed Event -> Truck: TRUCK-1020, Temperature: 20.11°C
Processed Event -> Truck: TRUCK-1046, Temperature: 22.09°C
Processed Event -> Truck: TRUCK-1043, Temperature: 28.79°C
Processed Event -> Truck: TRUCK-1032, Temperature: 24.48°C

This confirmed that the Faust processor was continuously receiving and processing streaming data from Kafka.

11. Testing Performed

The following tests were performed during Week 2:

Test 1 — Python Environment

Verified Python version:

py -3.11 --version

Result:

Python 3.11.9
Test 2 — Faust Installation

Verified Faust:

py -3.11 -c "import faust; print(faust.__version__)"

Result:

0.13.2
Test 3 — Kafka Availability

Kafka container was started using:

docker start kafka

Kafka was confirmed to be running on:

localhost:9092
Test 4 — Producer

The producer successfully generated continuous telemetry events.

Test 5 — Faust Processor

The Faust processor successfully consumed and processed the events from Kafka.

12. Week 2 Outcome

Week 2 was successfully completed.

The Stream Forge project now has a working real-time stream processing layer using Faust.

The system can:

Receive continuous truck telemetry from Kafka.
Consume events from the stream-events topic.
Process telemetry using Faust.
Display processed truck information in real time.
Maintain continuous communication between the Kafka producer and Faust processor.
Final Status
Week 1: Kafka Producer & Consumer       ✅ Completed
Week 2: Faust Stream Processing         ✅ Completed