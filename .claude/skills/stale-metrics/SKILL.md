# Stale Metrics Check

Use this skill when the user asks about stale metrics, sensors that have gone quiet, missing data, or wants to audit which home automation series are no longer reporting.

## Execution

```bash
python3 /home/zwhite/home_automation/.claude/skills/stale-metrics/check.py
```

## Staleness Thresholds

| Family | Threshold | Rationale |
|---|---|---|
| `ping_*` | 30 min | Runs every ~10s |
| `rtl433_*` | 2 h | RF sensors report every 1–5 min |
| `weather_*` | 3 h | OWM updates hourly |
| `zigbee2mqtt_*` | 25 h | Battery sensors only report on change |
| `esphome_*` | 2 h | ESPHome reports continuously |

## Reporting

Present two sections:

**Stale series** — for each: age in hours, metric name, labels. Group by metric family. For each stale series, give a plain-English assessment:
- Is this sensor expected to be active? (cross-reference the known sensor inventory below)
- Is it a one-off device that was captured by the RF receiver but is no longer nearby?
- Is it a known device that has likely lost power or battery?

**Fresh series** — one-line summary count only (no need to list all of them unless the user asks).

## Known Sensor Inventory

Active sensors that should always be fresh:
- `rtl433_*` — Acurite-Tower (garden, backdoor), Acurite-6045M (shed), Cotech-367959 (outdoor), Nexus-TH (167)
- `ping_*` — internet.gw, darkstar.frop.org (and any LAN hosts currently configured in ping2mqtt)
- `weather_*` — all weather metrics (fed by openweathermaps2mqtt)
- `zigbee2mqtt_*` — bathroom/bedroom/lily humidity_temp sensors, lily/office motion sensors, bedroom/diningroom switches

One-off / transient devices that may appear stale and can be flagged for deletion:
- TPMS sensors (tire pressure — these were captured from nearby vehicles)
- Springfield-Soil (soil moisture sensor — may be seasonal)
- Interlogix-Security (neighbour's alarm system, probably)
- Nexus-TH sensor "167" (unknown origin — only appears intermittently)
