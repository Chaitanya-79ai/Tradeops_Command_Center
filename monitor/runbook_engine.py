

RUNBOOKS = {
    "DATABASE_UNREACHABLE": [
        "Check database process",
        "Restart database service",
        "Check database logs",
        "Rerun pre-market check",
    ],
    "MARKET_DATA_TICK_UNAVAILABLE": [
        "Check market data service health endpoint",
        "Restart market data service",
        "Verify latest tick timestamp",
        "Inform trading desk if unresolved",
    ],
    "SERVICE_UNREACHABLE": [
        "Check if the service process is running",
        "Restart the affected service",
        "Verify the service health endpoint",
        "Check recent logs for errors",
    ],
    "HIGH_LATENCY": [
        "Check service response time",
        "Check CPU and memory usage",
        "Review logs for latency warnings",
        "Restart the affected service if latency stays high",
    ],
    "CPU_USAGE_HIGH": [
        "Check running processes",
        "Identify process using high CPU",
        "Restart unhealthy service if needed",
        "Monitor CPU usage again",
    ],
    "MEMORY_USAGE_HIGH": [
        "Check memory usage by process",
        "Stop unnecessary local processes",
        "Restart memory-heavy service if needed",
        "Monitor memory usage again",
    ],
    "DISK_USAGE_HIGH": [
        "Check logs directory size",
        "Remove or archive old logs",
        "Delete temporary files if safe",
        "Confirm disk usage is below threshold",
    ],
    "LOG_ERRORS_FOUND": [
        "Open logs/trading.log",
        "Review ERROR and CRITICAL messages",
        "Identify affected service",
        "Fix the issue and rerun monitor",
    ],
}


def get_runbook(issue_key):
    return RUNBOOKS.get(issue_key, ["No runbook available for this issue"])