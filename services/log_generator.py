import time
import random
from datetime import datetime

LOG_FILE = "logs/trading.log"
LOG_MESSAGES = [
    "INFO Market data tick received for NIFTY",
    "INFO Order accepted for NIFTY",
    "WARN Order latency high",
    "ERROR Database connection failed",
    "CRITICAL Market data stale"
]

def write_log():
    timestamp = datetime.now().isoformat()
    message = random.choice(LOG_MESSAGES)

    with open(LOG_FILE, "a") as file:
        file.write(f"{timestamp} {message}\n")

while True:
    write_log()
    time.sleep(2)