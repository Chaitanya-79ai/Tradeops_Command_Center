import sqlite3

DB_FILE = "data/tradeops.db"

connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS service_health (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT NOT NULL,
    status TEXT NOT NULL,
    checked_at TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    severity TEXT NOT NULL,
    service TEXT NOT NULL,
    issue TEXT NOT NULL,
    impact TEXT NOT NULL,
    created_at TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS premarket_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    final_status TEXT NOT NULL,
    reason TEXT,
    checked_at TEXT NOT NULL
)
""")

connection.commit()
connection.close()

print("Database initialized successfully")