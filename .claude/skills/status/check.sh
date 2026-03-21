#!/bin/bash
SERVICES=(
  victoria-metrics grafana-server homebridge
  mqtt2discord mqtt2graphite mqtt_triggers
  nginx openweathermaps2mqtt ping2mqtt
)

for svc in "${SERVICES[@]}"; do
  state=$(systemctl is-active "$svc")
  printf "%-30s %s\n" "$svc" "$state"
done

echo ""

for svc in "${SERVICES[@]}"; do
  state=$(systemctl is-active "$svc")
  if [ "$state" != "active" ]; then
    echo "=== $svc ($state) ==="
    journalctl -u "$svc" -n 30 --no-pager
    echo ""
  fi
done
