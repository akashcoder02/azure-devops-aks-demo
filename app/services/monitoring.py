import subprocess


def _run(command):

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10
        )

        return result

    except Exception:

        return None


def get_prometheus_status():

    result = _run([
        "kubectl",
        "get",
        "pods",
        "-n",
        "monitoring",
        "-l",
        "app.kubernetes.io/name=prometheus",
        "--no-headers"
    ])

    if result and result.returncode == 0 and result.stdout.strip():
        return "Running"

    return "Stopped"


def get_grafana_status():

    result = _run([
        "kubectl",
        "get",
        "pods",
        "-n",
        "monitoring",
        "-l",
        "app.kubernetes.io/name=grafana",
        "--no-headers"
    ])

    if result and result.returncode == 0 and result.stdout.strip():
        return "Running"

    return "Stopped"