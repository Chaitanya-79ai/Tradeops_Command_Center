from datetime import datetime
from database.db_manager import save_alert

ALERT_LOG_FILE = "data/alerts.log"

created_alerts = set()


def create_alert(severity, service, issue, impact, suggested_actions):
    alert_key = f"{severity}:{service}:{issue}"
    if alert_key in created_alerts:
        return
    created_alerts.add(alert_key)
    timestamp = datetime.now().isoformat()

    actions_text = "\n".join(
        f"{i+1}. {action}"
        for i, action in enumerate(suggested_actions)
    )

    alert_message = f"""
{severity} ALERT
Time: {timestamp}
Service: {service}
Issue: {issue}
Impact: {impact}
Suggested Action:
{actions_text}
"""

    print(alert_message)

    with open(ALERT_LOG_FILE, "a") as file:
        file.write(alert_message + "\n")

    save_alert(severity, service, issue, impact)
