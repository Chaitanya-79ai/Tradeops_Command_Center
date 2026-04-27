

RUNBOOKS = {
    "DATABASE_UNREACHABLE": [
        "Check database process",
        "Restart database service",
        "Rerun pre-market check",
    ],
    "MARKET_DATA_TICK_UNAVAILABLE": [
        "Check market data service health endpoint",
        "Restart market data service",
        "Verify latest tick timestamp",
        "Inform trading desk if unresolved",
    ],
}


def get_runbook(issue_key):
    return RUNBOOKS.get(issue_key, ["No runbook available for this issue"])