---
name: decommission
description: Use this skill when the user wants to decommission, remove, or retire a systemd service from this system.
version: 1.0.0
---

# Decommission a Service

When the user asks to decommission a service, follow these steps.

## Phase 1: Discover

Before doing anything, gather the facts:

1. Check service status: `systemctl status <service>`
2. Find the unit file: `find /etc/systemd /lib/systemd -name '*<service>*'`
3. Find the code directory: `find /home/zwhite -maxdepth 2 -name '*<service>*'`
4. Check for references to the path in other configs: `grep -r "<service>" /etc/ /home/zwhite/home_automation/`

Report what you found — service state, unit file location, code directory, and any references elsewhere.

## Phase 2: Confirm approach

The standard decommission pattern for this system is:
- **Code directory** → move to `/home/zwhite/attic/`
- **System unit file** → removed automatically by `systemctl disable` (services here use "linked" units)
- **No code deletion** — attic is the archive, not the trash

If the service is currently **active**, stop and ask the user to confirm before proceeding — stopping a running service may have side effects.

If there are references to the service path in other config files, flag them and ask how to handle before proceeding.

## Phase 3: Execute (one step at a time)

```bash
# 1. Disable and remove the unit file
sudo systemctl disable <service>

# 2. Move code to attic
mv /home/zwhite/<service-dir> /home/zwhite/attic/<service-dir>

# 3. Reload systemd
sudo systemctl daemon-reload
```

## Phase 4: Verify

```bash
systemctl status <service>         # should: "could not be found"
ls /home/zwhite/attic/<service-dir>  # should: show files
```

Report the results of both checks.

## Notes

- If the unit file is **not** "linked" (i.e., it's a package-managed file in `/lib/systemd/`), do not delete it — flag this to the user instead.
- If there is no code directory (binary-only service), skip the attic step and note it.
- If the service has a venv or build artifacts that bloat the attic, mention it and ask if the user wants to strip them before archiving.
