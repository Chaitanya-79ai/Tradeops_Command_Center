from datetime import datetime

ALERT_LOG_FILE = "data/alerts.log"


def create_alert(severity, service, issue, impact, suggested_actions):
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




