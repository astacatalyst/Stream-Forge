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

@app.get("/workers")
def get_workers():
    return [
        {"id": "worker-1", "label": "Worker 1", "status": "healthy"},
        {"id": "worker-2", "label": "Worker 2", "status": "healthy"},
        {"id": "worker-3", "label": "Worker 3", "status": "down"},
    ]