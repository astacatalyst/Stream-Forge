from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/topology")
def get_topology():
    return {
        "source": {"id": "fastapi-source", "label": "FastAPI: Data Source"},
        "dashboard": {"id": "dashboard-node", "label": "React Flow Dashboard (You are here)"},
        "kafka": {"id": "kafka-topic", "label": "Kafka: truck-telemetry"},
        "partitions": [
            {"id": "partition-0", "label": "Partition 0", "lag": 12},
            {"id": "partition-1", "label": "Partition 1", "lag": 3},
            {"id": "partition-2", "label": "Partition 2", "lag": 45},
        ],
        "workers": [
            {"id": "worker-1", "label": "Worker 1", "status": "healthy", "partition": "partition-0", "eventsPerSec": 1200},
            {"id": "worker-2", "label": "Worker 2", "status": "healthy", "partition": "partition-1", "eventsPerSec": 980},
            {"id": "worker-3", "label": "Worker 3", "status": "down", "partition": "partition-2", "eventsPerSec": 0},
        ],
    }

import random
import time

@app.get("/telemetry")
def get_telemetry():
    trucks = ["truck-1", "truck-2", "truck-3"]
    now = time.time()
    data = []
    for truck_id in trucks:
        readings = []
        for i in range(10):
            readings.append({
                "time": now - (9 - i) * 5,
                "temp": round(random.uniform(30, 90), 1)
            })
        data.append({"truck_id": truck_id, "readings": readings})
    return data

@app.get("/nodes-analysis")
def get_nodes_analysis():
    workers = [
        {"id": "worker-1", "label": "Worker 1", "status": "healthy", "eventsPerSec": 1200, "uptime": "2h 14m"},
        {"id": "worker-2", "label": "Worker 2", "status": "healthy", "eventsPerSec": 980, "uptime": "2h 14m"},
        {"id": "worker-3", "label": "Worker 3", "status": "down", "eventsPerSec": 0, "uptime": "0m"},
    ]
    total = len(workers)
    healthy = len([w for w in workers if w["status"] == "healthy"])
    return {
        "total": total,
        "healthy": healthy,
        "down": total - healthy,
        "workers": workers,
    }

@app.get("/locations")
def get_locations():
    return [
        {"truck_id": "TRUCK-1001", "lat": 17.38, "lng": 78.48, "status": "moving", "speed": 62},
        {"truck_id": "TRUCK-1003", "lat": 17.42, "lng": 78.44, "status": "moving", "speed": 45},
        {"truck_id": "TRUCK-1005", "lat": 17.35, "lng": 78.52, "status": "idle", "speed": 0},
        {"truck_id": "TRUCK-1008", "lat": 17.40, "lng": 78.39, "status": "moving", "speed": 58},
        {"truck_id": "TRUCK-1009", "lat": 17.36, "lng": 78.46, "status": "moving", "speed": 70},
    ]