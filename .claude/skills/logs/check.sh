#!/bin/bash
# Collect potentially concerning log entries for review

SERVICES=(
  victoria-metrics grafana-server homebridge
  mqtt2graphite mqtt_triggers
  nginx openweathermaps2mqtt ping2mqtt
  hestia-shed mosquitto
)

SINCE="24 hours ago"

# Home automation service warnings/errors
for svc in "${SERVICES[@]}"; do
  echo "=== SERVICE: $svc ==="
  out=$(journalctl -u "$svc" --since "$SINCE" -p warning --no-pager 2>/dev/null)
  if [ -z "$out" ]; then
    echo "(no warnings)"
  else
    echo "$out"
  fi
  echo ""
done

# Kernel errors / OOM kills
echo "=== KERNEL ERRORS ==="
out=$(journalctl -k --since "$SINCE" -p err --no-pager 2>/dev/null)
if [ -z "$out" ]; then
  echo "(no entries)"
else
  echo "$out"
fi
echo ""

# SSH failed logins / auth warnings
echo "=== SSH / AUTH ==="
out=$(journalctl -u ssh --since "$SINCE" -p warning --no-pager 2>/dev/null)
if [ -z "$out" ]; then
  echo "(no entries)"
else
  echo "$out"
fi
echo ""

# System auth log (covers sudo, su, PAM)
echo "=== SYSTEM AUTH LOG ==="
if [ -f /var/log/auth.log ]; then
  out=$(grep -iE "(fail|error|invalid|refused|denied)" /var/log/auth.log | tail -50)
  if [ -z "$out" ]; then
    echo "(no entries)"
  else
    echo "$out"
  fi
else
  echo "(auth.log not found)"
fi
echo ""

# nginx error log
echo "=== NGINX ERROR LOG ==="
if [ -f /var/log/nginx/error.log ]; then
  out=$(tail -50 /var/log/nginx/error.log)
  if [ -z "$out" ]; then
    echo "(no entries)"
  else
    echo "$out"
  fi
else
  echo "(nginx error.log not found)"
fi
echo ""
