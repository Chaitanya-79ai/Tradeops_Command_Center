import json
import os
import time
import requests
import psutil
from datetime import datetime
from monitor.alert_manager import create_alert

STATUS_FILE = "data/status.json"
LOG_FILE = "logs/trading.log"

SERVICE_URLS = {
    "market_data": "http://127.0.0.1:8001/health",
    "risk_service": "http://127.0.0.1:8002/health",
    "order_gateway": "http://127.0.0.1:8003/health"
}
TICK_URL = "http://127.0.0.1:8001/tick"

def check_service(url):
    try:
        start_time = datetime.now()
        response = requests.get(url, timeout=2)
        end_time = datetime.now()

        latency_ms = int((end_time - start_time).total_seconds() * 1000)

        if response.status_code == 200:
            return "OK", latency_ms
        else:
            return "FAIL", latency_ms

    except requests.exceptions.RequestException:
        return "FAIL", None
    
def get_last_tick_time():
    try:
        response = requests.get(TICK_URL, timeout=2)

        if response.status_code == 200:
            tick_data = response.json()
            return tick_data.get("timestamp")

        return None

    except requests.exceptions.RequestException:
        return None
    
while True:
    market_data_status, market_data_latency = check_service(SERVICE_URLS["market_data"])
    risk_service_status, risk_service_latency = check_service(SERVICE_URLS["risk_service"])
    order_gateway_status, order_gateway_latency = check_service(SERVICE_URLS["order_gateway"])

    services = {
        "market_data": market_data_status,
        "risk_service": risk_service_status,
        "order_gateway": order_gateway_status,
        "database": "FAIL"
    }

    latency_ms = {
        "market_data": market_data_latency,
        "risk_service": risk_service_latency,
        "order_gateway": order_gateway_latency
    }

    system = {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent
    }

    error_count = 0

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as file:
            for line in file:
                if "ERROR" in line or "CRITICAL" in line:
                    error_count += 1

    last_tick_time = get_last_tick_time()

    overall_status = "READY" if all(value == "OK" for value in services.values()) else "DEGRADED"

    alerts = []

    if last_tick_time is None:
        alerts.append("Market data tick unavailable")

        create_alert(
            severity="CRITICAL",
            service="Market Data",
            issue="Market data tick unavailable",
            impact="Trading should not start without live market data",
            suggested_actions=[
                "Check market data service health endpoint",
                "Restart market data service",
                "Verify latest tick timestamp"
            ]
        )

    for service_name, service_status in services.items():
        if service_status != "OK":
            alerts.append(f"{service_name} is unreachable")

            if service_name == "database":
                create_alert(
                    severity="CRITICAL",
                    service="Database",
                    issue="Database unreachable",
                    impact="Trading should not start",
                    suggested_actions=[
                        "Check database process",
                        "Restart database service",
                        "Rerun pre-market check"
                    ]
                )
    for service_name, latency in latency_ms.items():
        if latency is not None and latency > 100:
            alerts.append(f"{service_name} latency high")

            create_alert(
                severity="WARN",
                service=service_name,
                issue=f"High latency detected: {latency} ms",
                impact="Trading system response may be slow",
                suggested_actions=[
                    "Check service health endpoint",
                    "Check system CPU and memory usage",
                    "Review logs for latency warnings"
                ]
            )

    if system["cpu_percent"] > 80:
        alerts.append("CPU usage high")

    if system["memory_percent"] > 90:
        alerts.append("Memory usage high")

    if system["disk_percent"] > 80:
        alerts.append("Disk usage high")

    if error_count > 0:
        alerts.append(f"{error_count} log errors found")

    readiness_score = 100

    for service_status in services.values():
        if service_status != "OK":
            readiness_score -= 25

    if error_count > 0:
        readiness_score -= 10

    if system["cpu_percent"] > 80:
        readiness_score -= 10

    if system["memory_percent"] > 90:
        readiness_score -= 10

    if system["disk_percent"] > 80:
        readiness_score -= 10

    readiness_score = max(readiness_score, 0)

    status = {
        "overall_status": overall_status,
        "services": services,
        "system": system,
        "latency_ms": latency_ms,
        "error_count": error_count,
        "order_rejection_rate": 0,
        "last_tick_time": last_tick_time,
        "alerts": alerts,
        "readiness_score": readiness_score,
        "last_updated": datetime.now().isoformat()
    }

    os.makedirs("data", exist_ok=True)

    with open(STATUS_FILE, "w") as file:
        json.dump(status, file, indent=2)

    print("status.json updated")
    time.sleep(2)