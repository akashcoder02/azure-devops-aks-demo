import json
from pathlib import Path

reports_dir = Path(".")
output = {
    "findings": []
}

for report in sorted(reports_dir.glob("temp-*.json")):
    try:
        with open(report) as f:
            data = json.load(f)

        if isinstance(data, list):
            output["findings"].extend(data)

        elif isinstance(data, dict):
            output["findings"].append(data)

    except Exception:
        pass

with open(
    "reports/security/application/kubernetes/kubernetes.json",
    "w"
) as f:
    json.dump(
        output,
        f,
        indent=2
    )
