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


def get_cluster_status():

    result = _run(["kubectl", "cluster-info"])

    if result and result.returncode == 0:
        return "Running"

    return "Stopped"


def get_node_count():

    result = _run(["kubectl", "get", "nodes", "--no-headers"])

    if result and result.returncode == 0:

        return len(result.stdout.strip().splitlines())

    return 0


def get_pod_count():

    result = _run([
        "kubectl",
        "get",
        "pods",
        "--all-namespaces",
        "--no-headers"
    ])

    if result and result.returncode == 0:

        return len(result.stdout.strip().splitlines())

    return 0


def get_deployments():

    result = _run([
        "kubectl",
        "get",
        "deployments",
        "--all-namespaces",
        "--no-headers"
    ])

    if result and result.returncode == 0:

        return len(result.stdout.strip().splitlines())

    return 0


def get_services():

    result = _run([
        "kubectl",
        "get",
        "svc",
        "--all-namespaces",
        "--no-headers"
    ])

    if result and result.returncode == 0:

        return len(result.stdout.strip().splitlines())

    return 0


def get_ingress():

    result = _run([
        "kubectl",
        "get",
        "ingress",
        "--all-namespaces",
        "--no-headers"
    ])

    if result and result.returncode == 0:

        return len(result.stdout.strip().splitlines())

    return 0


def get_hpa():

    result = _run([
        "kubectl",
        "get",
        "hpa",
        "--all-namespaces",
        "--no-headers"
    ])

    if result and result.returncode == 0:

        return len(result.stdout.strip().splitlines())

    return 0