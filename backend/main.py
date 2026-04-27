import json
from fastapi import FastAPI
from monitor.runbook_engine import get_runbook

app = FastAPI()


STATUS_FILE = "data/status.json"
ALERTS_FILE = "data/alerts.log"


@app.get("/health")
def health_check():
    return {
        "status": "OK",
        "service": "backend"
    }


@app.get("/status")
def get_status():
    try:
        with open(STATUS_FILE, "r") as file:
            status_data = json.load(file)

        return status_data
    except FileNotFoundError:
        return {
            "error": "status file not found"
        }


# Alerts endpoint
@app.get("/alerts")
def get_alerts():
    try:
        with open(ALERTS_FILE, "r") as file:
            alerts = file.readlines()

        return {
            "alerts": alerts
        }
    except FileNotFoundError:
        return {
            "alerts": []
        }


# Runbook endpoint
@app.get("/runbook/{issue}")
def get_runbook_steps(issue):
    return {
        "issue": issue,
        "steps": get_runbook(issue)
    }
