import faust

app = faust.App(
    "stream-forge-processor",
    broker="kafka://localhost:9092",
    store="memory://"
)


class StreamEvent(faust.Record, serializer="json"):
    truck_id: str
    temperature: float
    timestamp: str


stream_events = app.topic(
    "stream-events",
    value_type=StreamEvent
)


@app.agent(stream_events)
async def process_events(events):
    async for event in events:
        print(
            f"Processed Event -> "
            f"Truck: {event.truck_id}, "
            f"Temperature: {event.temperature}°C, "
            f"Timestamp: {event.timestamp}"
        )


if __name__ == "__main__":
    app.main()