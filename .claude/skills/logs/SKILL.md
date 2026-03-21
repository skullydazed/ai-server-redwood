---
name: logs
description: Use this skill when the user asks to check logs, look for errors, find anything concerning, review recent issues, or asks "anything I should be worried about?" in the logs.
version: 1.0.0
---

# Log Review

When the user asks to review logs or check for concerns, run:

```bash
/home/zwhite/home_automation/.claude/skills/logs/check.sh
```

## Reporting

Parse the output and present a consolidated report grouped by severity:

### Action needed
Issues that require attention: service crashes, exec failures, OOM kills, brute-force attacks exceeding a threshold (>20 attempts from one IP in a session), repeated connection refusals to MQTT or other local services.

### Worth watching
Low-level noise that may warrant monitoring: occasional SSH probes (normal for a public IP), isolated connection resets, single transient errors.

### All clear
If a section has no entries, note it briefly.

## Noise to suppress (do not flag these)
- Routine SSH `kex_exchange_identification: Connection closed by remote host` — normal internet background noise for a public-facing host. Flag only if volume is extremely high (>50 in 24h) or if they come with brute-force auth attempts.
- Homebridge cosmetic warnings about accessory characteristics.

## Seasonal rule
Do not flag missing logs or inactivity for `hestia-shed` between Oct 15 and Mar 15 — the service is intentionally off during that period.

## Format
- Lead with the severity group that has findings
- For each finding: **service/source**, plain-English description, and the relevant raw log lines
- Keep it scannable — one paragraph per issue max
