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

The script prints each service's state, logs for any non-active services, and a `=== RESOURCES ===` section with disk, inode, memory, load, and CPU count data.

## Reporting

Parse the script output and present a single consolidated report:

1. Note which services are not `active`.
2. Present a single consolidated report:
   - Active services: one-line list
   - Each non-active service: status (`inactive`/`failed`) + 1–2 sentence plain-English summary of the root cause from the logs (e.g. "missing virtualenv", "config file not found", "connection refused to broker")

## Resources

After the service report, append a resource summary from the `=== RESOURCES ===` section.

**Thresholds — flag these as concerns:**
- **Disk:** any filesystem >80% full
- **Inodes:** any filesystem >80% inode usage
- **Memory:** available RAM <500MB
- **Load:** 15-minute load average > number of CPU cores
- **Uptime:** >30 days → suggest applying updates and rebooting

**Format:**
- All clear: one line, e.g. `Resources: disk 2%, inodes <1%, mem 2.5G/15G used, load 0.01`
- Any threshold exceeded: call it out as a separate concern with the specific value

## Seasonal / Expected-Inactive Services

Do not mention these services at all during their off-season — not in the active list, not as inactive, not with any parenthetical note. Treat them as if they do not exist.

| Service | Active season | Notes |
|---|---|---|
| `hestia-shed` | Oct 15 – Mar 15 | Requires manual hardware setup; never auto-start |
