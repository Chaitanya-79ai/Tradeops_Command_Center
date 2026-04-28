

# API Documentation

## Base URL

Local backend URL:

```text
http://127.0.0.1:8000
```

Docker backend URL:

```text
http://127.0.0.1:8000
```

## Interactive API Docs

When the backend is running, open:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

## GET /health

Checks whether the backend API is running.

### Request

```bash
curl http://127.0.0.1:8000/health
```

### Response

```json
{
  "status": "OK",
  "service": "backend"
}
```

## GET /status

Returns the latest TradeOps system status from `data/status.json`.

### Request

```bash
curl http://127.0.0.1:8000/status
```

### Example Response

```json
{
  "overall_status": "READY",
  "services": {
    "market_data": "OK",
    "risk_service": "OK",
    "order_gateway": "OK",
    "database": "OK"
  },
  "system": {
    "cpu_percent": 10.5,
    "memory_percent": 59.5,
    "disk_percent": 8.6
  },
  "latency_ms": {
    "market_data": 6,
    "risk_service": 4,
    "order_gateway": 5
  },
  "error_count": 0,
  "order_rejection_rate": 0,
  "last_tick_time": "2026-04-29T03:58:55.230685",
  "alerts": [],
  "readiness_score": 100,
  "last_updated": "2026-04-29T03:58:55.234177"
}
```

### Missing File Response

If `data/status.json` is missing:

```json
{
  "error": "status file not found"
}
```

## GET /alerts

Returns alerts from `data/alerts.log`.

### Request

```bash
curl http://127.0.0.1:8000/alerts
```

### Example Response

```json
{
  "alerts": [
    "CRITICAL ALERT\n",
    "Service: Market Data\n",
    "Issue: Market data tick unavailable\n"
  ]
}
```

### Missing File Response

If `data/alerts.log` is missing:

```json
{
  "alerts": []
}
```

## GET /runbook/{issue}

Returns runbook steps for a known issue key.

### Request

```bash
curl http://127.0.0.1:8000/runbook/DATABASE_UNREACHABLE
```

### Example Response

```json
{
  "issue": "DATABASE_UNREACHABLE",
  "steps": [
    "Check database process",
    "Restart database service",
    "Check database logs",
    "Rerun pre-market check"
  ]
}
```

## Supported Runbook Issue Keys

```text
DATABASE_UNREACHABLE
MARKET_DATA_TICK_UNAVAILABLE
SERVICE_UNREACHABLE
HIGH_LATENCY
CPU_USAGE_HIGH
MEMORY_USAGE_HIGH
DISK_USAGE_HIGH
LOG_ERRORS_FOUND
```