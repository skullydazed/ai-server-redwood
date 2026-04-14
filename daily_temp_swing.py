#!/usr/bin/env python3
"""Daily temperature swing for outdoor sensor (Cotech-367959) from VictoriaMetrics."""

import requests
from datetime import datetime, timezone
import time

from milc import cli

VM_URL = "http://localhost:8428"
METRIC = {
    'C': 'rtl433_temperature_C{model="Cotech-367959",channel="main",sensor="outdoor"}',
    'F': 'rtl433_temperature_F{model="Cotech-367959",channel="main",sensor="outdoor"}',
}

local_tz = datetime.now(timezone.utc).astimezone().tzinfo
start = datetime(2026, 3, 23, tzinfo=local_tz)
end = datetime.now(local_tz)

start_ts = int(start.timestamp())
end_ts = int(end.timestamp())


def query_range(expr):
    r = requests.get(
        f"{VM_URL}/api/v1/query_range",
        params={"query": expr, "start": start_ts, "end": end_ts, "step": "1d"},
    )
    r.raise_for_status()
    data = r.json()
    results = data["data"]["result"]
    if not results:
        return {}
    return {int(ts): float(val) for ts, val in results[0]["values"]}


@cli.argument('-C', action='store_const', dest='unit', const='C', help='Use Celsius (default)')
@cli.argument('-F', action='store_const', dest='unit', const='F', help='Use Fahrenheit')
@cli.entrypoint('Show daily temperature swing.')
def main(cli):
    unit = cli.args.unit or 'C'
    metric = METRIC[unit]
    mins = query_range(f"min_over_time({metric}[1d])")
    maxs = query_range(f"max_over_time({metric}[1d])")

    all_ts = sorted(set(mins) | set(maxs))

    print(f"{'Date':<12} {f'Min°{unit}':>7} {f'Max°{unit}':>7} {f'Swing°{unit}':>8}")
    print("-" * 38)

    for ts in all_ts:
        day = datetime.fromtimestamp(ts, tz=local_tz).date()
        if ts in mins and ts in maxs:
            lo = mins[ts]
            hi = maxs[ts]
            swing = hi - lo
            print(f"{str(day):<12} {lo:>7.1f} {hi:>7.1f} {swing:>8.1f}")

if __name__ == '__main__':
    cli()
