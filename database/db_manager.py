import sqlite3
from datetime import datetime

DB_FILE = "data/tradeops.db"


def save_service_health(service_name, status):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO service_health (service_name, status, checked_at)
        VALUES (?, ?, ?)
        """,
        (service_name, status, datetime.now().isoformat())
    )

    connection.commit()
    connection.close()


def check_database_health():
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        connection.close()
        return "OK"
    except sqlite3.Error:
        return "FAIL"



def save_alert(severity, service, issue, impact):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO alerts (severity, service, issue, impact, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (severity, service, issue, impact, datetime.now().isoformat())
    )

    connection.commit()
    connection.close()