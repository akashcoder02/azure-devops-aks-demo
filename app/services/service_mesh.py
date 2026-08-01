import json
import subprocess
from datetime import datetime
from services.github import trigger_workflow


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
        "get",
        "deployment",
        "istiod",
        "-n",
        "istio-system",
        "-o",
        "json"
    ])

    if not result or result.returncode != 0:
        return "Not Installed"

    try:

        data = json.loads(result.stdout)

        image = data["spec"]["template"]["spec"]["containers"][0]["image"]

        return image.split(":")[-1]

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

    statuses = [c["status"] for c in components]

    if all(s == "Running" for s in statuses):
        health = "Healthy"

    elif any(s == "Not Installed" for s in statuses):
        health = "Not Installed"

    else:
        health = "Warning"

    gateways_list = get_gateways()

    virtual_services_list = get_virtual_services()

    destination_rules_list = get_destination_rules()

    return {

        "version": get_istio_version(),

        "health": health,

        "gateways": get_gateway_count(),

        "virtual_services": get_virtual_service_count(),

        "destination_rules": get_destination_rule_count(),

        "applications": get_mesh_application_count(),

        "gateways_list": gateways_list,

        "virtual_services_list": virtual_services_list,

        "destination_rules_list": destination_rules_list,

        "components": components,

        "last_updated": datetime.now().strftime("%d %b %Y %I:%M:%S %p"),

    }

def get_traffic_management():
    """
    Returns all traffic management resources.
    """

    gateways = get_gateways()
    virtual_services = get_virtual_services()
    destination_rules = get_destination_rules()

    return {
        "summary": {
            "gateways": len(gateways),
            "virtual_services": len(virtual_services),
            "destination_rules": len(destination_rules),
            "applications": len(virtual_services)
        },
        "gateways": gateways,
        "virtual_services": virtual_services,
        "destination_rules": destination_rules
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
            "name": item["metadata"]["name"],
            "hosts": ", ".join(
                item.get("spec", {})
                    .get("servers", [{}])[0]
                    .get("hosts", [])
            ),
            "port": item.get("spec", {})
                        .get("servers", [{}])[0]
                        .get("port", {})
                        .get("number", "-"),
            "selector": item.get("spec", {})
                            .get("selector", {})
                            .get("istio", "-"),
            "status": "Healthy"
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
            "application": item["metadata"]["name"],
            "name": item["metadata"]["name"],
            "gateway": item.get("spec", {}).get("gateways", ["-"])[0],
            "host": item.get("spec", {}).get("hosts", ["-"])[0],
            "route": item.get("spec", {})
                        .get("http", [{}])[0]
                        .get("match", [{}])[0]
                        .get("uri", {})
                        .get("regex", "-"),
            "subset": item.get("spec", {})
                        .get("http", [{}])[0]
                        .get("route", [{}])[0]
                        .get("destination", {})
                        .get("subset", "-"),
            "weight": item.get("spec", {})
                        .get("http", [{}])[0]
                        .get("route", [{}])[0]
                        .get("weight", 0),
            "retry": item.get("spec", {})
                        .get("http", [{}])[0]
                        .get("retries", {})
                        .get("attempts", 0),
            "timeout": item.get("spec", {})
                        .get("http", [{}])[0]
                        .get("timeout", "-"),
            "status": "Healthy"
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
            "application": item["metadata"]["name"],
            "host": item.get("spec", {}).get("host", "-"),
            "subset": item.get("spec", {})
                        .get("subsets", [{}])[0]
                        .get("name", "-"),
            "load_balancer": item.get("spec", {})
                                .get("trafficPolicy", {})
                                .get("loadBalancer", {})
                                .get("simple", "-"),
            "max_connections": item.get("spec", {})
                                .get("trafficPolicy", {})
                                .get("connectionPool", {})
                                .get("tcp", {})
                                .get("maxConnections", "-"),
            "max_retries": item.get("spec", {})
                                .get("trafficPolicy", {})
                                .get("connectionPool", {})
                                .get("http", {})
                                .get("maxRetries", "-"),
            "idle_timeout": item.get("spec", {})
                                .get("trafficPolicy", {})
                                .get("connectionPool", {})
                                .get("http", {})
                                .get("idleTimeout", "-"),
            "status": "Healthy"
        }
        for item in data.get("items", [])
    ]


# ==========================================================
# TRAFFIC SHIFT
# ==========================================================

# ==========================================================
# SHIFT TRAFFIC
# ==========================================================

def shift_traffic(payload):

    application = payload.get("application")

    service_port = str(payload.get("service_port"))

    primary_version = payload.get("primary_version")

    primary_weight = str(payload.get("primary_weight"))

    canary_version = payload.get("canary_version")

    canary_weight = str(payload.get("canary_weight"))

    canary_enabled = str(
        payload.get("canary_enabled")
    ).lower()

    return trigger_workflow(

        workflow_file="traffic-shift.yml",

        inputs={

            "application": application,

            "service_port": service_port,

            "primary_version": primary_version,

            "primary_weight": primary_weight,

            "canary_version": canary_version,

            "canary_weight": canary_weight,

            "canary_enabled": canary_enabled

        }

    )

# ==========================================================
# CANARY DEPLOYMENT
# ==========================================================

def start_canary():

    return trigger_workflow(

        workflow_file="canary-deployment.yml"

    )


# ==========================================================
# ROLLBACK
# ==========================================================

def rollback_traffic():

    return trigger_workflow(

        workflow_file="rollback.yml"

    )

# ==========================================================
# APPLICATION CONFIGURATION
# ==========================================================

def get_application_configuration(application):

    applications = {

        "tic-tac-toe": {

            "application": "tic-tac-toe",

            "service_port": 80,

            "primary": {

                "version": "v1",

                "weight": 100

            },

            "canary": {

                "version": "v2",

                "weight": 0

            },

            "canary_enabled": False

        },

        "tetris": {

            "application": "tetris",

            "service_port": 80,

            "primary": {

                "version": "v1",

                "weight": 100

            },

            "canary": {

                "version": "v2",

                "weight": 0

            },

            "canary_enabled": False

        }

    }

    return applications.get(application)