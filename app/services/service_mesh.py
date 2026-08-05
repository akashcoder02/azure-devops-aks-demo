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

    services = []

    for item in data.get("items", []):

        routes = item.get("spec", {}).get("http", [{}])[0].get("route", [])

        for route in routes:

            services.append({

                "application": item["metadata"]["name"],

                "name": item["metadata"]["name"],

                "gateway": item.get("spec", {}).get("gateways", ["-"])[0],

                "host": item.get("spec", {}).get("hosts", ["-"])[0],

                "route": item.get("spec", {})
                            .get("http", [{}])[0]
                            .get("match", [{}])[0]
                            .get("uri", {})
                            .get("regex", "-"),

                "subset": route.get("destination", {}).get("subset", "-"),

                "weight": route.get("weight", 0),

                "retry": item.get("spec", {})
                            .get("http", [{}])[0]
                            .get("retries", {})
                            .get("attempts", 0),

                "timeout": item.get("spec", {})
                            .get("http", [{}])[0]
                            .get("timeout", "-"),

                "status": "Healthy"

            })

    return services

def get_security_destination_rules():

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

    canary_enabled = bool(payload.get("canary_enabled", False))


    return trigger_workflow(

        workflow_file="traffic-shift.yml",

        inputs={

            "application": application,

            "service_port": service_port,

            "primary_version": primary_version,

            "primary_weight": primary_weight,

            "canary_version": canary_version,

            "canary_weight": canary_weight,

            "canary_enabled": canary_enabled,

        }

    )

# ==========================================================
# CANARY DEPLOYMENT
# ==========================================================

def get_latest_image_tag(application):

    result = _run([
        "az",
        "acr",
        "repository",
        "show-tags",
        "--name",
        "agdevopsacr2026",
        "--repository",
        application,
        "--output",
        "tsv"
    ])

    if not result or result.returncode != 0:
        raise Exception("Unable to fetch image tags from ACR.")

    tags = [
        tag.strip()
        for tag in result.stdout.splitlines()
        if tag.strip()
    ]

    if not tags:
        raise Exception("No image tags found.")

    return tags[-1]

def start_canary(payload):

    application = payload.get("application")

    latest_image = get_latest_image_tag(application)

    return trigger_workflow(

        workflow_file="canary-deployment.yml",

        inputs={

            "application": application,

            "image_tag": latest_image,

            "replicas": str(payload.get("replicas", 1)),

            "service_port": str(payload.get("service_port", 80)),

            "primary_version": payload.get("primary_version", "v1"),

            "canary_version": payload.get("canary_version", "v2")


        }

    )

# ==========================================================
# ROLLBACK
# ==========================================================

def rollback_traffic(payload):

    return trigger_workflow(

        workflow_file="rollback-traffic.yml",

        inputs={

            "application": payload.get("application")

        }

    )
# ==========================================================
# APPLICATION CONFIGURATION
# ==========================================================

def get_application_configuration(application):

    result = _run([
        "kubectl",
        "get",
        "virtualservice",
        application,
        "-n",
        "default",
        "-o",
        "json"
    ])

    if not result or result.returncode != 0:
        return None

    data = json.loads(result.stdout)

    routes = data["spec"]["http"][0]["route"]

    primary = routes[0]
    canary = routes[1]

    return {

        "application": application,

        "service_port": primary["destination"]["port"]["number"],

        "primary": {

            "version": primary["destination"]["subset"],

            "weight": primary["weight"]

        },

        "canary": {

            "version": canary["destination"]["subset"],

            "weight": canary["weight"]

        },

        "canary_enabled": canary["weight"] > 0

    }

# ==========================================================
# SECURITY
# ==========================================================

# ==========================================================
# SECURITY HELPERS
# ==========================================================

def get_mtls_status():

    return {

        "mode": "STRICT",

        "namespace": "default",

        "peer_authentication": "Configured",

        "destination_rule": "ISTIO_MUTUAL"

    }


def get_peer_authentication():

    result = _run([
        "kubectl",
        "get",
        "peerauthentication",
        "--all-namespaces",
        "-o",
        "json"
    ])

    if not result or result.returncode != 0:
        return []

    data = json.loads(result.stdout)

    peer_authentications = []

    for item in data.get("items", []):

        peer_authentications.append({

            "namespace": item["metadata"]["namespace"],

            "mode": item.get("spec", {})
                        .get("mtls", {})
                        .get("mode", "UNSET"),

            "status": "Configured",

            "age": item["metadata"]["creationTimestamp"]

        })

    return peer_authentications

def get_authorization_policies():

    result = _run([
        "kubectl",
        "get",
        "authorizationpolicy",
        "--all-namespaces",
        "-o",
        "json"
    ])

    if not result or result.returncode != 0:
        return []

    data = json.loads(result.stdout)

    policies = []

    for item in data.get("items", []):

        policies.append({

            "name": item["metadata"]["name"],

            "namespace": item["metadata"]["namespace"],

            "action": item.get("spec", {}).get("action", "ALLOW"),

            "selector": ", ".join(
                item.get("spec", {})
                    .get("selector", {})
                    .get("matchLabels", {})
                    .keys()
            ) or "-",

            "status": "Configured"

        })

    return policies

def get_request_authentication():

    result = _run([
        "kubectl",
        "get",
        "requestauthentication",
        "--all-namespaces",
        "-o",
        "json"
    ])

    if not result or result.returncode != 0:

        return {

            "issuer": "--",

            "jwks_uri": "--",

            "workloads": 0,

            "status": "Disabled"

        }

    data = json.loads(result.stdout)

    items = data.get("items", [])

    if not items:

        return {

            "issuer": "--",

            "jwks_uri": "--",

            "workloads": 0,

            "status": "Disabled"

        }

    jwt = items[0].get("spec", {}).get("jwtRules", [{}])[0]

    return {

        "issuer": jwt.get("issuer", "--"),

        "jwks_uri": jwt.get("jwksUri", "--"),

        "workloads": len(items),

        "status": "Enabled"

    }


def get_workloads():

    workloads = []

    for sidecar in get_sidecars():

        workloads.append({

            "application": sidecar["application"],

            "namespace": sidecar["namespace"],

            "sidecar": sidecar["injected"],

            "mtls": "Enabled",

            "jwt": "Disabled",

            "authorization": "Enabled",

            "status": sidecar["status"]

        })

    return workloads


def get_sidecars():

    result = _run([
        "kubectl",
        "get",
        "pods",
        "--all-namespaces",
        "-o",
        "json"
    ])

    if not result or result.returncode != 0:
        return []

    data = json.loads(result.stdout)

    sidecars = []

    for item in data.get("items", []):

        containers = item.get("spec", {}).get("containers", [])

        istio_proxy = next(

            (c for c in containers if c["name"] == "istio-proxy"),

            None

        )

        sidecars.append({

            "pod": item["metadata"]["name"],

            "namespace": item["metadata"]["namespace"],

            "application": item["metadata"]["labels"].get("app", "-"),

            "injected": "Yes" if istio_proxy else "No",

            "ready": f'{item["status"].get("containerStatuses", [{}])[0].get("ready", False)}',

            "version": istio_proxy["image"].split(":")[-1] if istio_proxy else "-",

            "status": item["status"]["phase"]

        })

    return sidecars


def get_certificates_summary():

    certificates = get_certificates()

    return {

        "root_ca": "Healthy",

        "total": len(certificates),

        "expiring": 0,

        "rotation": "Enabled"

    }


def get_certificates():

    result = _run([
        "kubectl",
        "get",
        "secret",
        "--all-namespaces",
        "-o",
        "json"
    ])

    if not result or result.returncode != 0:
        return []

    data = json.loads(result.stdout)

    certificates = []

    for item in data.get("items", []):

        if item["type"] != "kubernetes.io/tls":
            continue

        certificates.append({

            "workload": item["metadata"]["namespace"],

            "name": item["metadata"]["name"],

            "issued": "-",

            "expires": "-",

            "days_left": "-",

            "status": "Healthy"

        })

    return certificates


def get_namespaces():

    result = _run([
        "kubectl",
        "get",
        "namespace",
        "-o",
        "json"
    ])

    if not result or result.returncode != 0:
        return []

    data = json.loads(result.stdout)

    namespaces = []

    for item in data.get("items", []):

        labels = item["metadata"].get("labels", {})

        namespaces.append({

            "name": item["metadata"]["name"],

            "injection": labels.get(

                "istio-injection",

                "disabled"

            ),

            "mtls": "Configured",

            "authorization": "Enabled",

            "jwt": "Disabled",

            "status": "Healthy"

        })

    return namespaces


def get_validation():

    validation = []

    validation.append({

        "name": "PeerAuthentication",

        "status": "OK" if get_peer_authentication() else "Missing"

    })

    validation.append({

        "name": "AuthorizationPolicy",

        "status": "OK" if get_authorization_policies() else "Missing"

    })

    validation.append({

        "name": "RequestAuthentication",

        "status": "OK" if get_request_authentication()["status"] == "Enabled" else "Disabled"

    })

    return validation


def get_security_events():

    return []

# ==========================================================
# SECURITY
# ==========================================================

def get_security():

    return {

        "summary": {

        "last_updated": datetime.now().strftime("%d %b %Y %I:%M:%S %p"),

        "mtls": get_mtls_status()["mode"],

        "authorization_policies": len(get_authorization_policies()),

        "certificates": get_certificates_summary()["root_ca"],

        "jwt": get_request_authentication()["status"],

        "sidecars": f"{len(get_sidecars())} Injected",

        "security_score": "Healthy"

    },

        "mtls": get_mtls_status(),

        "peer_authentication": get_peer_authentication(),

        "destination_rules": get_security_destination_rules(),

        "authorization_policies": get_authorization_policies(),

        "jwt": get_request_authentication(),

        "workloads": get_workloads(),

        "sidecars": get_sidecars(),

        "certificates_summary": get_certificates_summary(),

        "certificates": get_certificates(),

        "namespaces": get_namespaces(),

        "validation": get_validation(),

        "events": get_security_events()

    }

# ==========================================================
# RESILIENCE HELPERS
# ==========================================================

def get_retry_policies():

    policies = []

    for item in get_virtual_services():

        if item["retry"] != 0:

            policies.append({

                "application": item["application"],

                "attempts": item["retry"],

                "per_try_timeout": item["timeout"],

                "retry_on": "5xx,gateway-error,connect-failure",

                "status": "Configured"

            })

    return policies


def get_timeout_policies():

    timeouts = []

    for item in get_virtual_services():

        timeouts.append({

            "application": item["application"],

            "timeout": item["timeout"],

            "current": item["timeout"],

            "status": "Configured"

        })

    return timeouts


def get_circuit_breakers():

    breakers = []

    for item in get_security_destination_rules():

        breakers.append({

            "application": item["application"],

            "max_connections": item["max_connections"],

            "max_requests": item["max_retries"],

            "pending_requests": "-",

            "status": "Enabled"

        })

    return breakers


def get_connection_pools():

    pools = []

    for item in get_security_destination_rules():

        pools.append({

            "application": item["application"],

            "http_pool": item["max_retries"],

            "tcp_pool": item["max_connections"],

            "idle_timeout": item["idle_timeout"],

            "status": "Configured"

        })

    return pools


def get_outlier_detection():

    outliers = []

    for item in get_security_destination_rules():

        outliers.append({

            "application": item["application"],

            "errors": "5",

            "interval": "30s",

            "ejection": "5m",

            "status": "Enabled"

        })

    return outliers


def get_fault_injection():

    return []


def get_chaos_tests():

    return []


def get_resilience_score():

    return "100%"


# ==========================================================
# RESILIENCE
# ==========================================================

# ==========================================================
# APPLY RESILIENCE
# ==========================================================

def apply_resilience(payload):

    return trigger_workflow(

        workflow_file="service-mesh-resilience.yml",

        inputs=payload

    )


# ==========================================================
# RESET RESILIENCE
# ==========================================================

def reset_resilience():

    return trigger_workflow(

        workflow_file="service-mesh-resilience.yml",

        inputs={

            "action": "reset"

        }

    )

def get_resilience():

    return {

        "summary": {

            "last_updated": datetime.now().strftime("%d %b %Y %I:%M:%S %p"),

            "retry_policies": len(get_retry_policies()),

            "timeouts": len(get_timeout_policies()),

            "circuit_breakers": len(get_circuit_breakers()),

            "connection_pools": len(get_connection_pools()),

            "outlier_detection": len(get_outlier_detection()),

            "resilience_score": get_resilience_score()

        },

        "retry_policies": get_retry_policies(),

        "timeouts": get_timeout_policies(),

        "circuit_breakers": get_circuit_breakers(),

        "connection_pools": get_connection_pools(),

        "outlier_detection": get_outlier_detection(),

        "fault_injection": get_fault_injection(),

        "chaos_tests": get_chaos_tests()

    }