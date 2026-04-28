

# HFT TradeOps Command Center

Pre-market readiness, live monitoring, alerting, and incident response for simulated trading systems.

## Project Summary

HFT TradeOps Command Center is a simulated trade operations platform that answers one important question:

> Are we ready to trade today?

This project simulates the kind of operational tooling used by Trade Operations / Production Support teams to check whether trading services are healthy before market open and during live trading hours.

The system monitors simulated trading services, runs pre-market readiness checks, raises alerts, stores health history in SQLite, provides runbook-based recovery suggestions, and shows the current system state in a dashboard.



## System Components

### Market Data Service

File: `services/market_data_service.py`

Purpose:

Simulates live market data.

Endpoints:

```text
GET /health
GET /tick
```

### Risk Service

File: `services/risk_service.py`

Purpose:

Checks simple order risk rules.

Endpoints:

```text
GET /health
POST /check-order
```

Risk limits:

```text
MAX_ORDER_QTY = 500
MAX_ORDER_VALUE = 1000000
```

### Order Gateway

File: `services/order_gateway.py`

Purpose:

Receives fake orders and checks them with the Risk Service before accepting or rejecting them.

Endpoints:

```text
GET /health
POST /order
```

### Log Generator

File: `services/log_generator.py`

Purpose:

Generates fake trading logs in:

```text
logs/trading.log
```

### Pre-Market Check Script

File: `scripts/premarket_check.sh`

Purpose:

Runs a readiness checklist before market open.

Checks include:

- Market Data Service reachability
- Risk Service reachability
- Order Gateway reachability
- SQLite database reachability
- Disk usage
- Memory usage
- Config file presence
- Risk limits file presence
- CRITICAL log errors

### Python Monitor

File: `monitor/monitor.py`

Purpose:

Continuously monitors system health and writes live status to:

```text
data/status.json
```

Run command:

```bash
python3 -m monitor.monitor
```

Important:

Do not run:

```bash
python3 monitor/monitor.py
```

The monitor should be run as a Python module because `monitor/` is a package.

### Alert Manager

File: `monitor/alert_manager.py`

Purpose:

Creates alerts when something goes wrong.

Current alert outputs:

- Terminal / console
- `data/alerts.log`
- SQLite `alerts` table
- Dashboard visibility

### Runbook Engine

File: `monitor/runbook_engine.py`

Purpose:

Maps issues to recovery steps.

### Backend API

File: `backend/main.py`

Purpose:

Provides FastAPI endpoints for status, alerts, and runbook data.

Endpoints:

```text
GET /health
GET /status
GET /alerts
GET /runbook/{issue}
```

### Streamlit Dashboard

File: `dashboard/app.py`

Purpose:

Displays live TradeOps status in a dashboard.

Dashboard shows:

- Overall Status
- Readiness Score
- Error Count
- Service Health
- System Metrics
- Service Latency
- Active Alerts
- Runbook Suggestions
- Detailed Alert Log
- Last Updated Timestamp

Dashboard URL:

```text
http://localhost:8501
```

## Database

This project uses SQLite for simplicity and reliability.

Database file: `data/tradeops.db`

Database setup file: `database/init_db.py`

Database helper file: `database/db_manager.py`

Tables:

```text
service_health
alerts
premarket_results
```

## Folder Structure

```text
TradeOps Engine/
│
├── backend/
│   └── main.py
│
├── config/
│   ├── trading_config.yaml
│   └── risk_limits.yaml
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── alerts.log
│   ├── status.json
│   └── tradeops.db
│
├── database/
│   ├── db_manager.py
│   └── init_db.py
│
├── logs/
│   └── trading.log
│
├── monitor/
│   ├── __init__.py
│   ├── alert_manager.py
│   ├── monitor.py
│   └── runbook_engine.py
│
├── scripts/
│   └── premarket_check.sh
│
├── services/
│   ├── log_generator.py
│   ├── market_data_service.py
│   ├── order_gateway.py
│   └── risk_service.py
│
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd "TradeOps Engine"
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the SQLite database

```bash
python3 database/init_db.py
```

Expected output:

```text
Database initialized successfully
```

## Running Locally Without Docker

Open separate terminals for each service.

### Start Market Data Service

```bash
python3 -m uvicorn services.market_data_service:app --port 8001 --reload
```

### Start Risk Service

```bash
python3 -m uvicorn services.risk_service:app --port 8002 --reload
```

### Start Order Gateway

```bash
python3 -m uvicorn services.order_gateway:app --port 8003 --reload
```

### Start Backend

```bash
python3 -m uvicorn backend.main:app --port 8000 --reload
```

### Start Monitor

```bash
python3 -m monitor.monitor
```

### Start Dashboard

```bash
streamlit run dashboard/app.py
```

Dashboard:

```text
http://localhost:8501
```

Backend API:

```text
http://localhost:8000
```

## Running With Docker

Start all services:

```bash
make docker-up
```

Or directly:

```bash
docker compose up --build
```

Stop all services:

```bash
make docker-down
```

Or directly:

```bash
docker compose down
```

Docker starts:

- Market Data Service
- Risk Service
- Order Gateway
- Backend
- Monitor
- Dashboard

Dashboard URL:

```text
http://localhost:8501
```

Backend health check:

```bash
curl http://127.0.0.1:8000/health
```

Backend status API:

```bash
curl http://127.0.0.1:8000/status
```

## Makefile Commands

```bash
make docker-up
```

Starts the full Docker Compose system.

```bash
make docker-down
```

Stops Docker Compose containers.

```bash
make premarket
```

Runs the pre-market readiness check.

```bash
make monitor
```

Runs the Python monitor locally.

```bash
make backend
```

Runs the FastAPI backend locally.

```bash
make dashboard
```

Runs the Streamlit dashboard locally.

## Demo Flow

### Step 1: Start the system

```bash
make docker-up
```

### Step 2: Open dashboard

```text
http://localhost:8501
```

Expected dashboard state:

```text
Overall Status: READY
Readiness Score: 100/100
Market Data: OK
Risk Service: OK
Order Gateway: OK
Database: OK
```

### Step 3: Run pre-market check

In another terminal:

```bash
make premarket
```

Expected result when services are healthy:

```text
FINAL STATUS: READY TO TRADE
```

If local memory usage is high, the script may return:

```text
FINAL STATUS: NOT READY
Reason: Memory usage high;
```

That is expected on memory-constrained local machines and demonstrates that the system detects resource risk.

### Step 4: Simulate a service failure

Stop one container, for example Market Data:

```bash
docker compose stop market-data
```

Wait a few seconds.

Then check status:

```bash
curl http://127.0.0.1:8000/status
```

Expected behavior:

```text
market_data: FAIL
Overall Status: DEGRADED
Alert: market_data is unreachable
```

The dashboard should also show the degraded status and relevant runbook suggestion.

### Step 5: Recover the service

```bash
docker compose start market-data
```

Wait a few seconds.

The monitor should detect recovery and return system status back to healthy.

## Important Runtime File Rule

Running the monitor, Docker Compose, or tests updates runtime files:

```text
data/status.json
data/alerts.log
logs/trading.log
data/tradeops.db
```


## Useful Test Commands

### Test service health

```bash
curl http://127.0.0.1:8001/health
curl http://127.0.0.1:8002/health
curl http://127.0.0.1:8003/health
```

### Test market tick

```bash
curl http://127.0.0.1:8001/tick
```

### Test backend status

```bash
curl http://127.0.0.1:8000/status
```

### Test database rows

```bash
sqlite3 data/tradeops.db "SELECT service_name, status, checked_at FROM service_health ORDER BY id DESC LIMIT 8;"
```

### Test alert rows

```bash
sqlite3 data/tradeops.db "SELECT severity, service, issue, impact, created_at FROM alerts ORDER BY id DESC LIMIT 5;"
```
