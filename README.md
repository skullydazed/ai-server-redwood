# home_automation

Home automation services running on `redwood`, a Debian 12 Linux router that doubles as a home automation hub. Each service is a Python microservice managed by systemd, with MQTT as the central message bus.

This repository is intended to be used along-side `claude`, the CLI interface to Claude Code.

## Architecture

All services connect to a local [mosquitto](https://mosquitto.org/) MQTT broker at `127.0.0.1:1883`. Services either publish data to MQTT topics, subscribe to topics to trigger actions, or both. Time-series data flows from MQTT into VictoriaMetrics (via Graphite protocol) and is visualized in Grafana. Push notifications are delivered via a self-hosted ntfy server.

```
OpenWeatherMap API ───────────────────────────────┐
                                                  ▼
Network hosts ──── ping2mqtt ──────────────── mosquitto (MQTT broker)
                                                  │
                         ┌────────────────────────┤
                         │                        │
                   mqtt2graphite            mqtt_triggers
                         │                  mqtt2discord
                         ▼                  mqtt_battery_watch
               VictoriaMetrics                hestia
                         │
                         ▼                    ntfy ──── mobile/browser
                      Grafana
```

## System Services

Infrastructure services that the microservices depend on. These are not managed in this repo.

| Service | Unit | Port | What it does |
|---|---|---|---|
| mosquitto | `mosquitto.service` | 1883 | MQTT broker — central message bus |
| nginx | `nginx.service` | 80, 8079 | Reverse proxy; configs in `/etc/nginx/sites-enabled/` |
| ntfy | `ntfy.service` | 2586 | Push notification server at `http://redwood.lan:2586`; auth required; upstream `ntfy.sh` for mobile delivery |
| VictoriaMetrics | `victoria-metrics.service` | — | Time-series DB with Graphite-compatible ingestion |
| Grafana | `grafana-server.service` | — | Dashboard UI backed by VictoriaMetrics |
| PostgreSQL | `postgresql@15-main.service` | — | Database backend for meshview |

## Services

| Directory | systemd unit | What it does |
|---|---|---|
| `hestia/` | `hestia-shed.service` | Thermostat: reads temperature probe, controls heater switch via MQTT. Topics: `heater/<name>/status`, `heater/<name>/set` |
| `mqtt_triggers/` | `mqtt_triggers.service` | Event-driven automation: motion-activated lights, door/window sensor alerts, bed light auto-off |
| `mqtt2discord/` | `mqtt2discord.service` | Forwards anything published to `discord/#` to a Discord webhook |
| `mqtt2graphite/` | `mqtt2graphite.service` | Buffers MQTT sensor readings and flushes to VictoriaMetrics every minute via Graphite protocol |
| `openweathermaps2mqtt/` | `openweathermaps2mqtt.service` | Fetches OpenWeatherMap forecast hourly and publishes flattened fields to `weather/*` |
| `ping2mqtt/` | `ping2mqtt.service` | Continuously pings configured hosts; publishes 10s/1m/5m rolling latency averages to `ping/*` |
| `mqtt_battery_watch/` | `mqtt_battery_watch.service` | Monitors charger power draw; publishes to `discord/bike_battery` when crossing a wattage threshold |

## Configuration

Each service is configured via environment variables set in its systemd unit file (typically in `/etc/systemd/system/<unit>.service` or an override). Common variables across services:

- `MQTT_HOST`, `MQTT_PORT`, `MQTT_USER`, `MQTT_PASS` — broker connection
- Service-specific topic and behavior settings

Each service directory has its own Python virtual environment at `.venv/` and a `requirements.txt`. All use `paho-mqtt<2`.

## Claude Skills

The `.claude/skills/` directory contains skill definitions used by Claude Code when running as a sysadmin assistant:

| Skill | Trigger | What it does |
|---|---|---|
| `status` | "status", "what's running" | Checks all service states; flags disk/memory/load issues |
| `logs` | "check logs", "anything concerning" | Reviews recent warnings/errors across services and system logs |
| `decommission` | "decommission \<service\>" | Guided workflow to safely retire a service and archive its code |

See `CLAUDE.md` for full system context and operating rules.

## Repo Notes

Service code directories (`hestia/`, `mqtt_triggers/`, etc.) are listed in `.gitignore` — each is a standalone environment managed independently. This repo tracks only:

- Claude skill definitions (`.claude/skills/`)
- `CLAUDE.md` — system context and sysadmin rules for Claude Code
- This README
