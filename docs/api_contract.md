# StreamForge — API Contract

All endpoints are served by the FastAPI backend at `http://localhost:8000`. CORS is configured to allow requests from the dashboard at `http://localhost:5173`.

---

## `GET /health`

Basic liveness check.

**Response**
```json
{ "status": "ok" }
```

---

## `GET /topology`

Returns the full pipeline topology for the DAG view: the API source node, the Kafka topic, its partitions, and the workers assigned to each partition.

**Response**
```json
{
  "source": { "id": "fastapi-source", "label": "FastAPI: Data Source" },
  "dashboard": { "id": "dashboard-node", "label": "React Flow Dashboard (You are here)" },
  "kafka": { "id": "kafka-topic", "label": "Kafka: truck-telemetry" },
  "partitions": [
    { "id": "partition-0", "label": "Partition 0", "lag": 12 }
  ],
  "workers": [
    {
      "id": "worker-1",
      "label": "Worker 1",
      "status": "healthy",
      "partition": "partition-0",
      "eventsPerSec": 1200
    }
  ]
}
```

`status` is one of: `healthy`, `down`.

---

## `GET /nodes-analysis`

Summary and detail view of worker health, used by the Working Nodes tab.

**Response**
```json
{
  "total": 3,
  "healthy": 2,
  "down": 1,
  "workers": [
    {
      "id": "worker-1",
      "label": "Worker 1",
      "status": "healthy",
      "eventsPerSec": 1200,
      "uptime": "2h 14m"
    }
  ]
}
```

---

## `GET /locations`

Simulated truck positions, used by the Location tab.

**Response**
```json
[
  {
    "truck_id": "TRUCK-1001",
    "lat": 17.38,
    "lng": 78.48,
    "status": "moving",
    "speed": 62
  }
]
```

`status` is one of: `moving`, `idle`.

---

## `GET /telemetry`

Mock time-series temperature readings per truck, used by the Temperature tab during development.

**Response**
```json
[
  {
    "truck_id": "truck-1",
    "readings": [
      { "time": 1723999999.0, "temp": 45.2 }
    ]
  }
]
```

---

## `GET /real-telemetry`

Live truck readings sourced from the actual Kafka `stream-events` topic via a background consumer thread. Returns the latest known reading per truck.

**Response**
```json
[
  {
    "truck_id": "TRUCK001",
    "temperature": 25.5,
    "timestamp": "2026-08-15T10:30:00+00:00"
  }
]
```

**Note:** this endpoint reflects whatever the Kafka producer has sent since the backend started — it will be empty until the producer runs at least once.

---

## Design Notes

- Every endpoint returns a fixed JSON shape regardless of whether the underlying data is mocked or real — this is the core API contract the dashboard is built against.
- `/telemetry` and `/nodes-analysis` currently serve mock data and are candidates to be swapped for real Kafka/Faust-sourced data, following the same pattern used for `/real-telemetry`.
- The upstream Kafka event shape (as published by the producer) is: `{ "truck_id": string, "temperature": float, "timestamp": ISO8601 string }`, published to topic `stream-events`.