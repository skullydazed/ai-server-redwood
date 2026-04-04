#!/usr/bin/env python3
"""Query VictoriaMetrics and report age of last data point for all home automation series."""

import json, time, urllib.request, urllib.parse, sys

VM = "http://localhost:8428"
NOW = time.time()

PREFIXES = ("rtl433_", "ping_", "weather_", "zigbee2mqtt_", "esphome_")

# Staleness thresholds in hours by metric family
THRESHOLDS = {
    "ping_":        0.5,   # ping runs every ~10s
    "rtl433_":      2.0,   # RF sensors report every 1-5 min
    "weather_":     3.0,   # OWM updates hourly
    "zigbee2mqtt_": 25.0,  # battery sensors only report on change
    "esphome_":     2.0,
}

def vm_query(query):
    params = urllib.parse.urlencode({"query": query})
    url = f"{VM}/api/v1/query?{params}"
    with urllib.request.urlopen(url, timeout=15) as r:
        return json.load(r)["data"]["result"]

def threshold_for(name):
    for prefix, hours in THRESHOLDS.items():
        if name.startswith(prefix):
            return hours
    return 2.0

results = vm_query('last_over_time({job="node", __name__!~"node_.*|go_.*|process_.*|apt_.*|nvme_.*|promhttp_.*|scrape_.*|up"}[30d])')

series = []
for m in results:
    name = m["metric"].get("__name__", "")
    if not any(name.startswith(p) for p in PREFIXES):
        continue
    ts = float(m["value"][0])
    age_h = (NOW - ts) / 3600
    labels = {k: v for k, v in m["metric"].items() if k not in ("__name__", "job", "instance")}
    series.append((age_h, name, labels))

series.sort(key=lambda x: x[0], reverse=True)

stale = [(a, n, l) for a, n, l in series if a > threshold_for(n)]
fresh = [(a, n, l) for a, n, l in series if a <= threshold_for(n)]

print(f"=== STALE ({len(stale)} series) ===")
if stale:
    for age, name, labels in stale:
        label_str = ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))
        threshold = threshold_for(name)
        print(f"  {age:6.1f}h  (threshold {threshold:.0f}h)  {name}{{{label_str}}}")
else:
    print("  (none)")

print()
print(f"=== FRESH ({len(fresh)} series) ===")
for age, name, labels in fresh:
    label_str = ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))
    print(f"  {age:6.1f}h  {name}{{{label_str}}}")
