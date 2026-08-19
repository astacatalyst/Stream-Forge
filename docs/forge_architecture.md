# StreamForge — Project Architecture

## Overview

StreamForge is a distributed, pure-Python stream processing system that ingests simulated IoT truck telemetry (temperature readings), processes it through Kafka and a Faust stream processor, and visualizes system health and truck data through a live web dashboard.

The system is built around a clear separation of concerns: producers generate data, Kafka carries it, a stream processor consumes and transforms it, and an API + dashboard layer makes the whole pipeline observable in real time.

## Team Ownership

| Area | Owner | Responsibility |
|---|---|---|
| Kafka Producer | Jyoti | Generates and streams simulated truck telemetry events into Kafka |
| Database / State | Jyoti | Persistent storage for processed truck data |
| Faust Stream Processor | Pooja | Consumes Kafka events, performs windowed aggregation (rolling averages), manages worker state |
| API + Dashboard | Priya (lead) | FastAPI backend, React Flow visualization, system-wide integration and testing |

## System Components

### 1. Kafka Message Broker
The foundational log that ingests and carries truck telemetry events. Runs locally via Docker (`docker-compose.yml`), using KRaft mode (no separate Zookeeper).

- **Topic:** `stream-events`
- **Broker address:** `localhost:9092`

### 2. Producer (Jyoti)
A Python script using `kafka-python` that publishes simulated truck telemetry — truck ID, temperature, and timestamp — to the `stream-events` topic.

### 3. Faust Stream Processor (Pooja)
Consumes events from `stream-events`, performs windowed aggregations (rolling average temperature per truck), and manages processing state. This is the layer responsible for detecting worker health and partition assignment.

### 4. FastAPI Backend (Priya)
The single source of truth for the frontend. Exposes a consistent set of REST endpoints (see `API_CONTRACT.md`) that abstract away whether underlying data is real (from Kafka/Faust) or mocked during development. Includes a background Kafka consumer thread that maintains an in-memory cache of the latest reading per truck.

### 5. React Flow Dashboard (Priya)
A tabbed web dashboard with four views:
- **Working Nodes** — worker count, health status, and per-worker throughput
- **Location** — simulated truck positions on a coordinate grid
- **Temperature** — live-updating line chart of per-truck temperature readings
- **DAG** — interactive topology diagram showing the full data flow: FastAPI → Kafka → Partitions → Workers

## Data Flow

```
Producer (Jyoti)
      │  publishes truck telemetry
      ▼
 Kafka Topic: stream-events
      │  consumed by
      ▼
Faust Stream Processor (Pooja)
      │  windowed aggregation, state
      ▼
FastAPI Backend (background consumer thread)
      │  serves JSON via REST endpoints
      ▼
React Flow Dashboard (live, auto-refreshing)
```

## Local Development Setup

1. Start Kafka: `docker compose up -d` (from project root)
2. Start backend: `cd backend && .\venv\Scripts\Activate.ps1 && python -m uvicorn main:app --reload`
3. Start frontend: `cd frontend && npm run dev`
4. Dashboard available at `http://localhost:5173`

## Design Principle: Mock-First Development

The dashboard was built against mock data first, with FastAPI endpoints returning hardcoded JSON matching the eventual real data shape. This allowed frontend and backend work to proceed independently of Kafka/Faust integration timelines, with real data swapped in once available — without any frontend code changes, since the API contract stayed fixed.