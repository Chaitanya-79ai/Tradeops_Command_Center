import json
import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from monitor.runbook_engine import get_runbook

STATUS_FILE = PROJECT_ROOT / "data" / "status.json"
ALERTS_FILE = PROJECT_ROOT / "data" / "alerts.log"

ALERT_TO_RUNBOOK_KEY = {
    "database is unreachable": "DATABASE_UNREACHABLE",
    "market_data is unreachable": "SERVICE_UNREACHABLE",
    "risk_service is unreachable": "SERVICE_UNREACHABLE",
    "order_gateway is unreachable": "SERVICE_UNREACHABLE",
    "market data tick unavailable": "MARKET_DATA_TICK_UNAVAILABLE",
    "logs contain error or critical entries": "LOG_ERRORS_FOUND",
}


def load_status():
    if not STATUS_FILE.exists():
        return None

    with open(STATUS_FILE, "r") as file:
        return json.load(file)


def load_alert_log():
    if not ALERTS_FILE.exists():
        return "No alert log found."

    content = ALERTS_FILE.read_text().strip()
    return content if content else "No detailed alerts logged yet."




st.set_page_config(
    page_title="HFT TradeOps Command Center",
    page_icon="⚡",
    layout="wide",
)


st.markdown(
    """
    <style>
    .main {
        background: #0f172a;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .title-box {
        background: linear-gradient(135deg, #111827, #1e293b);
        border: 1px solid #334155;
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .title-box h1 {
        color: #f8fafc;
        margin-bottom: 6px;
    }
    .title-box p {
        color: #94a3b8;
        margin-bottom: 0;
    }
    .status-card {
        background: #111827;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
    }
    .status-card h3 {
        color: #94a3b8;
        font-size: 15px;
        margin-bottom: 8px;
    }
    .status-card p {
        color: #f8fafc;
        font-size: 28px;
        font-weight: 800;
        margin: 0;
    }
    .ok {
        color: #22c55e;
        font-weight: 800;
    }
    .fail {
        color: #ef4444;
        font-weight: 800;
    }
    .muted {
        color: #94a3b8;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

status = load_status()

st.markdown(
    """
    <div class="title-box">
        <h1>⚡ HFT TradeOps Command Center</h1>
        <p>Pre-market readiness, live monitoring, alerting, and incident response for simulated trading systems.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if status is None:
    st.error("data/status.json not found. Start the monitor first using: python3 -m monitor.monitor")
    st.stop()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="status-card">
            <h3>Overall Status</h3>
            <p>{status.get("overall_status", "UNKNOWN")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="status-card">
            <h3>Readiness Score</h3>
            <p>{status.get("readiness_score", 0)}/100</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="status-card">
            <h3>Error Count</h3>
            <p>{status.get("error_count", 0)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

with st.expander("🧩 Service Health", expanded=True):
    services = status.get("services", {})
    for service_name, service_status in services.items():
        label = service_name.replace("_", " ").title()
        css_class = "ok" if service_status == "OK" else "fail"
        st.markdown(f"**{label}:** <span class='{css_class}'>{service_status}</span>", unsafe_allow_html=True)

with st.expander("🖥️ System Metrics"):
    system = status.get("system", {})
    col1, col2, col3 = st.columns(3)
    col1.metric("CPU", f'{system.get("cpu_percent", 0)}%')
    col2.metric("Memory", f'{system.get("memory_percent", 0)}%')
    col3.metric("Disk", f'{system.get("disk_percent", 0)}%')

with st.expander("⏱️ Service Latency"):
    latency = status.get("latency_ms", {})
    for service_name, latency_value in latency.items():
        label = service_name.replace("_", " ").title()
        st.write(f"**{label}:** {latency_value} ms")

with st.expander("🚨 Active Alerts", expanded=True):
    alerts = status.get("alerts", [])
    if not alerts:
        st.success("No active alerts")
    else:
        for alert in alerts:
            st.error(alert)

with st.expander("📘 Runbook Suggestions", expanded=True):
    alerts = status.get("alerts", [])
    if not alerts:
        st.info("No runbook needed because there are no active alerts.")
    else:
        for alert in alerts:
            st.subheader(alert)
            runbook_key = ALERT_TO_RUNBOOK_KEY.get(alert.lower(), alert.upper().replace(" ", "_"))
            for index, step in enumerate(get_runbook(runbook_key), start=1):
                st.write(f"{index}. {step}")

with st.expander("📄 Detailed Alert Log"):
    st.code(load_alert_log())

st.caption(f'Last updated: {status.get("last_updated", "unknown")}')