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
    destination_rules_list = get_security_destination_rules()

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
    destination_rules = get_security_destination_rules()

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

    try:
        data = json.loads(result.stdout)
    except Exception:
        return []

    services = []

    for item in data.get("items", []):
        http_rules = item.get("spec", {}).get("http", [])

        for rule in http_rules:
            retries = rule.get("retries", {})
            routes = rule.get("route", [])

            for route in routes:
                services.append({
                    "application": item["metadata"]["name"],
                    "name": item["metadata"]["name"],
                    "gateway": item.get("spec", {}).get("gateways", ["-"])[0],
                    "host": item.get("spec", {}).get("hosts", ["-"])[0],
                    "route": rule.get("match", [{}])[0]
                        .get("uri", {})
                        .get("regex", "-"),
                    "subset": route.get("destination", {}).get("subset", "-"),
                    "weight": route.get("weight", 0),
                    "retry": retries.get("attempts", 0),
                    "per_try_timeout": retries.get("perTryTimeout", "-"),
                    "retry_on": retries.get(
                        "retryOn",
                        "5xx,gateway-error,connect-failure,refused-stream"
                    ),
                    "timeout": rule.get("timeout", "-"),
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

    try:
        data = json.loads(result.stdout)
    except Exception:
        return []

    rules = []

    for item in data.get("items", []):
        spec = item.get("spec", {})
        policy = spec.get("trafficPolicy", {})
        pool = policy.get("connectionPool", {})
        tcp = pool.get("tcp", {})
        http = pool.get("http", {})
        outlier = policy.get("outlierDetection", {})

        rules.append({
            "application": item["metadata"]["name"],
            "host": spec.get("host", "-"),
            "subset": spec.get("subsets", [{}])[0].get("name", "-"),
            "load_balancer": policy.get(
                "loadBalancer", {}
            ).get("simple", "-"),

            "max_connections": tcp.get(
                "maxConnections", "-"
            ),

            "max_retries": http.get(
                "maxRetries", "-"
            ),

            "max_requests": http.get(
                "maxRequestsPerConnection", "-"
            ),

            "pending_requests": http.get(
                "http1MaxPendingRequests", "-"
            ),

            "idle_timeout": http.get(
                "idleTimeout", "-"
            ),

            "consecutive_errors": outlier.get(
                "consecutive5xxErrors", "-"
            ),

            "outlier_interval": outlier.get(
                "interval", "-"
            ),

            "base_ejection_time": outlier.get(
                "baseEjectionTime", "-"
            ),

            "outlier_configured": bool(outlier),

            "status": "Healthy"
        })

    return rules


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

def apply_security(payload):

    return trigger_workflow(

        workflow_file="service-mesh-security.yml",

        inputs=payload

    )


def destroy_security():

    return trigger_workflow(

        workflow_file="service-mesh-security.yml",

        inputs={

            "action": "destroy"

        }

    )

# ==========================================================
# RESILIENCE HELPERS
# ==========================================================

def get_retry_policies():
    """Return retry configuration from live Istio VirtualServices."""
    policies = []

    for item in get_virtual_services():
        if item.get("retry", 0):
            policies.append({
                "application": item["application"],
                "attempts": item.get("retry", 0),
                "per_try_timeout": item.get("per_try_timeout", "-"),
                "retry_on": item.get(
                    "retry_on",
                    "5xx,gateway-error,connect-failure,refused-stream"
                ),
                "status": "Configured"
            })

    return policies


def get_timeout_policies():
    """Return timeout configuration from live Istio VirtualServices."""
    timeouts = []

    for item in get_virtual_services():
        timeout = item.get("timeout", "-")

        timeouts.append({
            "application": item["application"],
            "timeout": timeout,
            "current": timeout,
            "status": "Configured" if timeout != "-" else "Not Configured"
        })

    return timeouts


def get_circuit_breakers():
    """Return live circuit-breaker connection limits."""
    breakers = []

    for item in get_security_destination_rules():
        breakers.append({
            "application": item["application"],
            "max_connections": item.get("max_connections", "-"),
            "pending_requests": item.get("pending_requests", "-"),
            "max_requests": item.get("max_requests", "-"),
            "status": "Enabled"
        })

    return breakers


def get_connection_pools():
    """Return live Istio connection-pool configuration."""
    pools = []

    for item in get_security_destination_rules():
        pools.append({
            "application": item["application"],
            "http_pool": item.get("max_requests", "-"),
            "tcp_pool": item.get("max_connections", "-"),
            "idle_timeout": item.get("idle_timeout", "-"),
            "status": "Configured"
        })

    return pools


def get_outlier_detection():
    """Return live Istio outlier-detection configuration."""
    outliers = []

    for item in get_security_destination_rules():
        configured = item.get("outlier_configured", False)

        outliers.append({
            "application": item["application"],
            "errors": item.get("consecutive_errors", "-"),
            "interval": item.get("outlier_interval", "-"),
            "ejection": item.get("base_ejection_time", "-"),
            "status": "Enabled" if configured else "Not Configured"
        })

    return outliers


def get_fault_injection():
    """Return live fault-injection VirtualServices."""
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

    try:
        data = json.loads(result.stdout)
    except Exception:
        return []

    faults = []

    for item in data.get("items", []):
        metadata = item.get("metadata", {})
        labels = metadata.get("labels", {})

        if labels.get("module") != "service-mesh-resilience":
            continue

        for rule in item.get("spec", {}).get("http", []):
            fault = rule.get("fault", {})

            if not fault:
                continue

            delay = fault.get("delay", {})
            abort = fault.get("abort", {})

            if delay and abort:
                fault_type = "Delay + Abort"
            elif delay:
                fault_type = "Delay"
            elif abort:
                fault_type = "Abort"
            else:
                fault_type = "None"

            faults.append({
                "application": labels.get(
                    "application",
                    metadata.get("name", "-").removesuffix("-fault")
                ),
                "type": fault_type,
                "delay": delay.get("fixedDelay", "-") if delay else "-",
                "delay_percentage": delay.get(
                    "percentage", {}
                ).get("value", 0) if delay else 0,
                "abort_status": abort.get(
                    "httpStatus", "-"
                ) if abort else "-",
                "abort_percentage": abort.get(
                    "percentage", {}
                ).get("value", 0) if abort else 0,
                "status": "Configured"
            })

    return faults


def _get_default_deployments():
    """Return application deployments from the default namespace."""
    result = _run([
        "kubectl",
        "get",
        "deployments",
        "-n",
        "default",
        "-o",
        "json"
    ])

    if not result or result.returncode != 0:
        return []

    try:
        return json.loads(result.stdout).get("items", [])
    except Exception:
        return []


def get_chaos_tests():
    """
    Report live workload state after chaos/recovery operations.

    Chaos actions themselves are executed by the GitHub workflow.
    Kubernetes does not retain a generic 'last chaos action' record, so
    this endpoint reports the current deployment state instead of
    inventing historical results.
    """
    deployments = _get_default_deployments()

    if not deployments:
        return []

    tests = []

    for deployment in deployments:
        metadata = deployment.get("metadata", {})
        spec = deployment.get("spec", {})
        status = deployment.get("status", {})

        name = metadata.get("name", "-")
        desired = spec.get("replicas", 0)
        available = status.get("availableReplicas", 0)
        ready = status.get("readyReplicas", 0)

        if desired == 0:
            state = "Scaled to Zero"
        elif available == desired and ready == desired:
            state = "Healthy"
        elif available > 0:
            state = "Recovering"
        else:
            state = "Unavailable"

        tests.append({
            "application": name,
            "restart": "Available",
            "delete_pod": "Available",
            "delete_all": "Available",
            "scale_zero": "Available",
            "recover": "Available",
            "current_state": state,
            "replicas": f"{available}/{desired}",
            "status": "Healthy" if state == "Healthy" else state
        })

    return tests


def get_resilience_score():
    """Calculate a live baseline resilience score."""
    checks = [
        bool(get_retry_policies()),
        bool(get_timeout_policies()),
        bool(get_circuit_breakers()),
        bool(get_connection_pools()),
        bool(get_outlier_detection()),
    ]

    score = round((sum(checks) / len(checks)) * 100) if checks else 0

    return f"{score}%"


# ==========================================================
# RESILIENCE
# ==========================================================

def _normalise_resilience_inputs(payload):
    """
    Normalize the UI payload for service-mesh-resilience.yml.

    Existing buttons can send only {"action": "..."} and the workflow
    defaults remain responsible for omitted values.
    """
    payload = payload or {}

    allowed = {
        "action",
        "retry_attempts",
        "per_try_timeout",
        "request_timeout",
        "max_connections",
        "max_requests_per_connection",
        "idle_timeout",
        "consecutive_errors",
        "outlier_interval",
        "base_ejection_time",
        "fault_delay_enabled",
        "fault_delay",
        "fault_delay_percentage",
        "fault_abort_enabled",
        "fault_abort_status",
        "fault_abort_percentage",
        "chaos_enabled",
        "chaos_action",
    }

    inputs = {
        key: payload[key]
        for key in allowed
        if key in payload and payload[key] is not None
    }

    inputs.setdefault("action", "defaults")

    return inputs


# ==========================================================
# APPLY RESILIENCE
# ==========================================================

def apply_resilience(payload):
    """Trigger the existing Service Mesh Resilience workflow."""
    return trigger_workflow(
        workflow_file="service-mesh-resilience.yml",
        inputs=_normalise_resilience_inputs(payload)
    )


# ==========================================================
# RESET RESILIENCE
# ==========================================================

def reset_resilience():
    """Trigger the existing Service Mesh Resilience reset action."""
    return trigger_workflow(
        workflow_file="service-mesh-resilience.yml",
        inputs={
            "action": "reset"
        }
    )


def get_resilience():
    """Return the complete live resilience dashboard payload."""
    retry_policies = get_retry_policies()
    timeouts = get_timeout_policies()
    circuit_breakers = get_circuit_breakers()
    connection_pools = get_connection_pools()
    outlier_detection = get_outlier_detection()
    fault_injection = get_fault_injection()
    chaos_tests = get_chaos_tests()

    return {
        "summary": {
            "last_updated": datetime.now().strftime(
                "%d %b %Y %I:%M:%S %p"
            ),
            "retry_policies": len(retry_policies),
            "timeouts": len(timeouts),
            "circuit_breakers": len(circuit_breakers),
            "connection_pools": len(connection_pools),
            "outlier_detection": len(outlier_detection),
            "fault_injection": len(fault_injection),
            "chaos_tests": len(chaos_tests),
            "resilience_score": get_resilience_score()
        },
        "retry_policies": retry_policies,
        "timeouts": timeouts,
        "circuit_breakers": circuit_breakers,
        "connection_pools": connection_pools,
        "outlier_detection": outlier_detection,
        "fault_injection": fault_injection,
        "chaos_tests": chaos_tests
    }