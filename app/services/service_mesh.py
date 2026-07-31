import json
import subprocess


# ==========================================================
# INTERNAL COMMAND EXECUTOR
# ==========================================================

def _run(command):

    try:

        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10
        )

    except Exception:

        return None


# ==========================================================
# ISTIO VERSION
# ==========================================================

def get_istio_version():

    result = _run([
        "kubectl",
        "version",
        "-o",
        "json"
    ])

    if not result or result.returncode != 0:
        return "Unknown"

    try:

        data = json.loads(result.stdout)

        return data["clientVersion"]["gitVersion"]

    except Exception:

        return "Unknown"


# ==========================================================
# ISTIOD STATUS
# ==========================================================

def get_istiod_status():

    result = _run([
        "kubectl",
        "get",
        "pods",
        "-n",
        "istio-system",
        "-l",
        "app=istiod",
        "--no-headers"
    ])

    if not result or result.returncode != 0:

        return {
            "name": "istiod",
            "namespace": "istio-system",
            "status": "Not Installed"
        }

    pods = result.stdout.strip().splitlines()

    if len(pods) == 0:

        return {
            "name": "istiod",
            "namespace": "istio-system",
            "status": "Not Found"
        }

    status = pods[0].split()[2]

    return {
        "name": "istiod",
        "namespace": "istio-system",
        "status": status
    }


# ==========================================================
# INGRESS GATEWAY
# ==========================================================

def get_ingress_gateway_status():

    result = _run([
        "kubectl",
        "get",
        "pods",
        "-n",
        "istio-system",
        "-l",
        "app=istio-ingressgateway",
        "--no-headers"
    ])

    if not result or result.returncode != 0:

        return {
            "name": "istio-ingressgateway",
            "namespace": "istio-system",
            "status": "Not Installed"
        }

    pods = result.stdout.strip().splitlines()

    if len(pods) == 0:

        return {
            "name": "istio-ingressgateway",
            "namespace": "istio-system",
            "status": "Not Found"
        }

    status = pods[0].split()[2]

    return {
        "name": "istio-ingressgateway",
        "namespace": "istio-system",
        "status": status
    }


# ==========================================================
# GATEWAYS
# ==========================================================

def get_gateway_count():

    result = _run([
        "kubectl",
        "get",
        "gateway",
        "--all-namespaces",
        "--no-headers"
    ])

    if not result or result.returncode != 0:
        return 0

    return len(result.stdout.strip().splitlines())


# ==========================================================
# VIRTUAL SERVICES
# ==========================================================

def get_virtual_service_count():

    result = _run([
        "kubectl",
        "get",
        "virtualservice",
        "--all-namespaces",
        "--no-headers"
    ])

    if not result or result.returncode != 0:
        return 0

    return len(result.stdout.strip().splitlines())


# ==========================================================
# DESTINATION RULES
# ==========================================================

def get_destination_rule_count():

    result = _run([
        "kubectl",
        "get",
        "destinationrule",
        "--all-namespaces",
        "--no-headers"
    ])

    if not result or result.returncode != 0:
        return 0

    return len(result.stdout.strip().splitlines())


# ==========================================================
# APPLICATION COUNT
# ==========================================================

def get_mesh_application_count():

    return get_virtual_service_count()


# ==========================================================
# OVERVIEW
# ==========================================================

def get_overview():

    components = [

        get_istiod_status(),

        get_ingress_gateway_status()

    ]

    healthy = all(

        component["status"] == "Running"

        for component in components

    )

    gateways_list = get_gateways()

    virtual_services_list = get_virtual_services()

    destination_rules_list = get_destination_rules()

    return {

        "version": get_istio_version(),

        "health": "Healthy" if healthy else "Warning",

        "gateways": get_gateway_count(),

        "virtual_services": get_virtual_service_count(),

        "destination_rules": get_destination_rule_count(),

        "applications": get_mesh_application_count(),

        "gateways_list": gateways_list,

        "virtual_services_list": virtual_services_list,

        "destination_rules_list": destination_rules_list,

        "components": components

    }

def get_traffic_management():
    """
    Returns all traffic management resources.
    """

    return {
        "gateways": get_gateways(),
        "virtual_services": get_virtual_services(),
        "destination_rules": get_destination_rules()
    }

def get_gateways():

    result = _run([
        "kubectl",
        "get",
        "gateway",
        "--all-namespaces",
        "-o",
        "json"
    ])

    if not result or result.returncode != 0:
        return []

    data = json.loads(result.stdout)

    return [
        {
            "namespace": item["metadata"]["namespace"],
            "name": item["metadata"]["name"]
        }
        for item in data.get("items", [])
    ]

def get_virtual_services():

    result = _run([
        "kubectl",
        "get",
        "virtualservice",
        "--all-namespaces",
        "-o",
        "json"
    ])

    if not result or result.returncode != 0:
        return []

    data = json.loads(result.stdout)

    return [
        {
            "namespace": item["metadata"]["namespace"],
            "name": item["metadata"]["name"]
        }
        for item in data.get("items", [])
    ]

def get_destination_rules():

    result = _run([
        "kubectl",
        "get",
        "destinationrule",
        "--all-namespaces",
        "-o",
        "json"
    ])

    if not result or result.returncode != 0:
        return []

    data = json.loads(result.stdout)

    return [
        {
            "namespace": item["metadata"]["namespace"],
            "name": item["metadata"]["name"]
        }
        for item in data.get("items", [])
    ]

