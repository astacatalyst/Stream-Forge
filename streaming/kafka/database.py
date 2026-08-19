import sqlite3

DB_NAME = "streamforge.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            truck_id TEXT NOT NULL,
            timestamp TEXT,
            temperature REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            truck_id TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            status TEXT,
            speed REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workers (
            id TEXT PRIMARY KEY,
            label TEXT,
            status TEXT,
            events_per_sec REAL,
            uptime TEXT
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
