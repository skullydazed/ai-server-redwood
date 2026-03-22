#!/bin/bash
SERVICES=(
  victoria-metrics grafana-server homebridge
  mqtt2discord mqtt2graphite mqtt_triggers mqtt_battery_watch
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

echo "=== RESOURCES ==="
echo "--- disk ---"
df -h --output=target,pcent,avail | grep -v tmpfs | tail -n +2
echo "--- inodes ---"
df -i | grep -v tmpfs | grep -v "^Filesystem" | awk '{print $6, $5, $4}'
echo "--- memory ---"
free -h | grep -E "Mem|Swap"
echo "--- load ---"
uptime
echo "--- cpu_count ---"
nproc
