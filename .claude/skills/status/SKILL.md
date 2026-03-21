---
name: status
description: Use this skill when the user asks for "status", "service status", "what's running", "are services up", or wants to check if home automation services are healthy.
version: 1.0.0
---

# Service Status Check

When the user asks for status, run:

```bash
/home/zwhite/home_automation/.claude/skills/status/check.sh
```

The script prints each service's state, then logs for any non-active services.

## Reporting

Parse the script output and present a single consolidated report:

1. Note which services are not `active`.
2. Present a single consolidated report:
   - Active services: one-line list
   - Each non-active service: status (`inactive`/`failed`) + 1–2 sentence plain-English summary of the root cause from the logs (e.g. "missing virtualenv", "config file not found", "connection refused to broker")

## Seasonal / Expected-Inactive Services

Do not mention these inactive services during their off-season:

| Service | Active season | Notes |
|---|---|---|
| `hestia-shed` | Oct 15 – Mar 15 | Requires manual hardware setup; never auto-start |
