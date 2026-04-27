

RUNBOOKS = {
    "DATABASE_UNREACHABLE": [
        "Check database process",
        "Restart database service",
        "Rerun pre-market check",
    ],
}


def get_runbook(issue_key):
    return RUNBOOKS.get(issue_key, ["No runbook available for this issue"])