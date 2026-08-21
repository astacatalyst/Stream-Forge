## StreamForge — Milestone Release

Repository: astacatalyst/streamforge

A distributed, pure-Python stream processing system for IoT truck telemetry, built as part of our internship project.

### What's included

**API + Dashboard**
- FastAPI backend with endpoints for health, topology, worker analysis, truck locations, and live telemetry
- React Flow-based dashboard with four views: Working Nodes, Location, Temperature, and an interactive DAG showing the full data pipeline
- Background Kafka consumer feeding real truck telemetry into the dashboard

**Kafka Pipeline**
- Producer and consumer scripts for IoT truck telemetry (truck ID, temperature, timestamp)
- Local Kafka setup via Docker (KRaft mode)

**Testing**
- Backend test suite (pytest) covering all API endpoints
- Frontend smoke tests (Vitest) for core dashboard rendering

**Documentation**
- `PROJECT_ARCHITECTURE.md` — system design and data flow
- `API_CONTRACT.md` — full endpoint reference
- `TEAM_RULES.md` — Git workflow and code review conventions

### Known limitations
- Producer currently sends a fixed set of sample events rather than a continuous stream
- Location and some temperature data are simulated, not sourced from real GPS/sensors
- Full Prometheus metrics integration is planned but not yet complete

### Team
Built by Priya (API + Dashboard, project lead), Jyoti (Kafka producer, database), and Pooja (Kafka consumer, stream processing).