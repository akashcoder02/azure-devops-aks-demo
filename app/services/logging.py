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


def get_fluentbit_status():

    result = _run([
        "kubectl",
        "get",
        "pods",
        "-n",
        "logging",
        "-l",
        "app.kubernetes.io/name=fluent-bit",
        "--no-headers"
    ])

    if result and result.returncode == 0 and result.stdout.strip():
        return "Running"

    return "Stopped"


def get_loki_status():

    result = _run([
        "kubectl",
        "get",
        "pods",
        "-n",
        "logging",
        "-l",
        "app.kubernetes.io/name=loki",
        "--no-headers"
    ])

    if result and result.returncode == 0 and result.stdout.strip():
        return "Running"

    return "Stopped"