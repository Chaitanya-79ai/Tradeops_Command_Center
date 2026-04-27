#!/bin/bash
#!/bin/bash

MARKET_DATA_URL="http://127.0.0.1:8001/health"
RISK_SERVICE_URL="http://127.0.0.1:8002/health"
ORDER_GATEWAY_URL="http://127.0.0.1:8003/health"

LOG_FILE="logs/trading.log"

OVERALL_STATUS="READY"

REASONS=""

echo "========== PRE-MARKET READINESS CHECK =========="


if curl -s "$MARKET_DATA_URL" > /dev/null; then
    echo "[OK] Market Data Service reachable"
else
    echo "[FAIL] Market Data Service not reachable"
    OVERALL_STATUS="NOT READY"
    REASONS="${REASONS}Market Data Service not reachable;"
fi

if curl -s "$RISK_SERVICE_URL" > /dev/null; then
    echo "[OK] Risk Service reachable"
else
    echo "[FAIL] Risk Service not reachable"
    OVERALL_STATUS="NOT READY"
    REASONS="${REASONS}Risk Service not reachable;"
fi

if curl -s "$ORDER_GATEWAY_URL" > /dev/null; then
    echo "[OK] Order Gateway reachable"
else
    echo "[FAIL] Order Gateway not reachable"
    OVERALL_STATUS="NOT READY"
    REASONS="${REASONS}Order Gateway not reachable;"
fi

DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')

if [ "$DISK_USAGE" -lt 80 ]; then
    echo "[OK] Disk usage below 80%"
else
    echo "[FAIL] Disk usage is ${DISK_USAGE}%"
    OVERALL_STATUS="NOT READY"
    REASONS="${REASONS}Disk usage high;"
fi

MEMORY_USAGE=$(vm_stat | awk '
/Pages active/ {active=$3}
/Pages wired down/ {wired=$4}
/Pages free/ {free=$3}
END {
  gsub("\\.","",active)
  gsub("\\.","",wired)
  gsub("\\.","",free)
  used=active+wired
  total=used+free
  printf "%.0f", (used/total)*100
}')

if [ "$MEMORY_USAGE" -lt 90 ]; then
    echo "[OK] Memory usage below 80%"
else
    echo "[FAIL] Memory usage is ${MEMORY_USAGE}%"
    OVERALL_STATUS="NOT READY"
    REASONS="${REASONS}Memory usage high;"
fi

if [ -f "config/trading_config.yaml" ] && [ -f "config/risk_limits.yaml" ]; then
    echo "[OK] Config files present"
else
    echo "[FAIL] Required config files missing"
    OVERALL_STATUS="NOT READY"
    REASONS="${REASONS}Required config files missing;"
fi

if grep -q "max_order_qty:" config/risk_limits.yaml && grep -q "max_order_value:" config/risk_limits.yaml; then
    echo "[OK] Risk limits file valid"
else
    echo "[FAIL] Risk limits file invalid"
    OVERALL_STATUS="NOT READY"
    REASONS="${REASONS}Risk limits file invalid;"
fi

if [ -f "$LOG_FILE" ] && grep -q "CRITICAL" "$LOG_FILE"; then
    echo "[FAIL] CRITICAL errors found in logs"
    OVERALL_STATUS="NOT READY"
    REASONS="${REASONS}CRITICAL errors found in logs;"
else
    echo "[OK] No CRITICAL errors found in logs"
fi

echo ""

if [ "$OVERALL_STATUS" = "READY" ]; then
    echo "FINAL STATUS: READY TO TRADE"
else
    echo "FINAL STATUS: NOT READY"
    echo "Reason: $REASONS"
fi

