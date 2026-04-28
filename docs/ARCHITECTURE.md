# Architecture Documentation

## High-Level Architecture

```text
                         ┌─────────────────────┐
                         │ Streamlit Dashboard │
                         │ Shows live status   │
                         └──────────▲──────────┘
                                    │
                                    │ reads shared runtime data
                                    │
                         ┌──────────┴──────────┐
                         │   FastAPI Backend   │
                         │ Exposes status APIs │
                         └──────────▲──────────┘
                                    │
                                    │ reads data/status.json
                                    │
             ┌──────────────────────┴──────────────────────┐
             │                                             │
   ┌─────────┴─────────┐                         ┌─────────┴─────────┐
   │  Python Monitor   │                         │ Bash Health Check │
   │  Live monitoring  │                         │ Pre-market check  │
   └─────────▲─────────┘                         └─────────▲─────────┘
             │                                             │
             └──────────────────────┬──────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
         ┌──────────┴──────────┐         ┌──────────┴──────────┐
         │ Simulated Trading   │         │ SQLite / Logs /     │
         │ Services            │         │ Config / Status     │
         └─────────────────────┘         └─────────────────────┘
```

## Component Relationships

```text
Market Data Service ─┐
Risk Service         ├──► Python Monitor ───► data/status.json ───► Backend / Dashboard
Order Gateway        ┘            │
                                  ├──► data/alerts.log
                                  ├──► SQLite service_health table
                                  └──► SQLite alerts table
```

## Data Flow

```text
1. Simulated trading services expose health and trading endpoints.
2. Python monitor checks service health, latency, database health, system metrics, and logs.
3. Monitor writes the latest status into data/status.json.
4. Alert manager writes incidents into data/alerts.log and SQLite.
5. Backend exposes status, alerts, and runbook data through APIs.
6. Streamlit dashboard reads runtime data and displays the command center view.
```

## Docker Architecture

```text
Docker Compose
│
├── market-data      → FastAPI service on port 8001
├── risk-service     → FastAPI service on port 8002
├── order-gateway    → FastAPI service on port 8003
├── backend          → FastAPI backend on port 8000
├── monitor          → Python live monitoring process
└── dashboard        → Streamlit dashboard on port 8501
```

## Shared Runtime Volumes

```text
./data:/app/data
./logs:/app/logs
```

These shared volumes allow the monitor, backend, and dashboard containers to use the same runtime files.

## Docker Networking

Inside Docker, the monitor uses Docker Compose service names:

```text
http://market-data:8001/health
http://risk-service:8002/health
http://order-gateway:8003/health
http://market-data:8001/tick
```

Locally, the monitor defaults to localhost URLs:

```text
http://127.0.0.1:8001/health
http://127.0.0.1:8002/health
http://127.0.0.1:8003/health
http://127.0.0.1:8001/tick
```

This difference is handled using environment variables in `docker-compose.yml`.

## Runtime Data Stores

```text
data/status.json      → latest system status

data/alerts.log       → formatted alert log

data/tradeops.db      → SQLite operational history

logs/trading.log      → simulated trading logs
```
