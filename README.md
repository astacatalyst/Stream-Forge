# StreamForge

StreamForge is a distributed stream-processing project for monitoring simulated IoT truck telemetry. It sends truck temperature events through Apache Kafka, exposes the processed data through a FastAPI backend, and displays the system through a React dashboard.

The project is designed to make a streaming pipeline easy to observe. A user can see worker health, Kafka partitions, truck locations, temperature readings, and the relationship between the services in one dashboard.

## What StreamForge Does

The system follows this flow:

```text
Kafka Producer -> Kafka topic -> Stream processor -> FastAPI -> React dashboard
```

1. The Kafka producer creates truck events containing a truck ID, temperature, and timestamp.
2. Kafka stores the events in the `stream-events` topic.
3. A stream processor consumes the events and is responsible for processing and aggregating the stream.
4. The FastAPI backend provides a stable REST API for the frontend. It also consumes live Kafka events and keeps the latest reading for each truck in memory.
5. The React dashboard periodically requests the API and presents the pipeline state visually.

## Main Features

- **Working Nodes:** Shows worker count, health, uptime, and throughput.
- **Location:** Shows simulated truck positions and movement status.
- **Temperature:** Shows temperature readings over time for each truck.
- **DAG:** Shows the path from FastAPI through Kafka partitions to workers.
- **Live telemetry:** The `/real-telemetry` endpoint returns the latest readings received from Kafka.
- **Mock-first development:** The dashboard can be developed and tested before the complete Kafka and stream-processing integration is available.

## Requirements

- Python 3.10 or newer
- Node.js and npm
- Apache Kafka running at `localhost:9092`
- A Kafka topic named `stream-events`

Kafka is expected to be started locally, commonly with Docker. If the project receives a `docker-compose.yml` file, Kafka can be started from the project root with:

```powershell
docker compose up -d
```

## How to Run the Project

### 1. Start Kafka

Start Kafka and make sure the broker is available at `localhost:9092`.

### 2. Start the backend

From the project root, activate the backend virtual environment and run FastAPI:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload
```

The backend is available at `http://localhost:8000`.

### 3. Start the frontend

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the dashboard at `http://localhost:5173`.

### 4. Send sample Kafka events

With Kafka running, use another terminal to publish sample telemetry:

```powershell
python streaming/kafka/producer.py
```

To inspect events directly instead, run:

```powershell
python streaming/kafka/consumer.py
```

After the producer sends events, refresh the dashboard or request `http://localhost:8000/real-telemetry` to see the latest readings received by the backend.

## Backend API

The backend currently provides these endpoints:

| Endpoint | Purpose |
|---|---|
| `GET /health` | Confirms that the backend is running |
| `GET /topology` | Returns Kafka partitions and worker topology |
| `GET /nodes-analysis` | Returns worker health and throughput |
| `GET /locations` | Returns simulated truck locations |
| `GET /telemetry` | Returns mock temperature time-series data |
| `GET /real-telemetry` | Returns the latest readings received from Kafka |

The response shapes are documented in [docs/api_contract.md](docs/api_contract.md). Keeping these shapes stable allows the frontend to work with mock data while the streaming implementation is being completed.

## Testing

The backend uses `pytest` and FastAPI's `TestClient`. The current tests verify that:

- `GET /health` returns HTTP 200 and `{ "status": "ok" }`.
- `GET /topology` returns HTTP 200 and includes Kafka, partition, and worker data.

Run the tests from the backend directory:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pytest
```

These are fast API smoke tests. They do not require a running Kafka broker because they test the HTTP endpoints directly. Future tests should cover the remaining endpoints, invalid data, Kafka event handling, and an end-to-end flow from producer to dashboard.

The frontend also has development checks:

```powershell
cd frontend
npm run lint
npm run build
```

## Development Approach

StreamForge uses a mock-first approach:

1. Define the API response shape in the API contract.
2. Return representative mock data from the backend.
3. Build and test the React dashboard against that stable contract.
4. Replace mock responses with Kafka or Faust-backed data without changing the frontend contract.
5. Add integration tests once the complete streaming path is available.

This keeps frontend, backend, Kafka, and stream-processing work independent while still giving the team a clear integration target.

## Documentation

- [Architecture](docs/forge_architecture.md)
- [API contract](docs/api_contract.md)
- [Team rules](docs/team_rules.md)