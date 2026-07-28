import json
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path


if len(sys.argv) < 2:
    exit(0)

path = Path(sys.argv[1])

try:
    with open(path) as f:
        data = json.load(f)

except Exception:
    data = {}

if isinstance(data, dict):

    data["scan_time"] = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime("%Y-%m-%d %H:%M:%S IST")

else:

    data = {
        "scan_time": datetime.now(
            ZoneInfo("Asia/Kolkata")
        ).strftime("%Y-%m-%d %H:%M:%S IST"),
        "findings": data
    }

with open(path, "w") as f:
    json.dump(
        data,
        f,
        indent=2
    )