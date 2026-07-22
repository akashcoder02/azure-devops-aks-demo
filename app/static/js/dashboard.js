// ========================================
// Azure Internal Developer Platform
// Dashboard
// ========================================

document.addEventListener("DOMContentLoaded", () => {

    bindButtons();

    loadDashboard();

    // Refresh dashboard every 30 seconds
    setInterval(loadDashboard, 30000);

});

// ========================================
// Button Events
// ========================================

function bindButtons() {

    document
        .getElementById("start-btn")
        ?.addEventListener("click", () => run("start"));

    document
        .getElementById("stop-btn")
        ?.addEventListener("click", () => run("stop"));

    document
        .getElementById("doctor-btn")
        ?.addEventListener("click", () => run("doctor"));

    document
        .getElementById("status-btn")
        ?.addEventListener("click", () => run("status"));

    document
        .getElementById("resources-btn")
        ?.addEventListener("click", () => run("resources"));

    document
        .getElementById("jobs-btn")
        ?.addEventListener("click", () => {

            window.location.href = "/platform/jobs";

        });

}

// ========================================
// Execute Platform Actions
// ========================================

async function run(action) {

    let url = "";

    switch (action) {

        case "start":
            url = "/api/platform/start";
            break;

        case "stop":
            url = "/api/platform/stop";
            break;

        case "doctor":
            url = "/api/platform/doctor";
            break;

        case "status":
            url = "/api/platform/status";
            break;

        case "resources":
            url = "/api/platform/resources";
            break;

        default:
            return;

    }

    try {

        const response = await fetch(url, {

            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }

        });

        const result = await response.json();

        alert(result.message || "Action completed.");

        // Refresh dashboard after action
        loadDashboard();

    } catch (error) {

        console.error(error);

        alert("Failed to execute platform action.");

    }

}

// ========================================
// Helpers
// ========================================

function updateText(id, value) {

    const element = document.getElementById(id);

    if (!element) return;

    element.textContent = value ?? "-";

}

function updateStatus(id, status) {

    const element = document.getElementById(id);

    if (!element) return;

    element.className = "";

    const value = (status || "").toUpperCase();

    switch (value) {

        case "RUNNING":
        case "CONNECTED":
        case "READY":
        case "HEALTHY":
        case "AVAILABLE":
            element.innerHTML = "🟢 " + status;
            element.classList.add("running");
            break;

        case "DEGRADED":
            element.innerHTML = "🟡 Degraded";
            element.classList.add("warning");
            break;

        case "STOPPED":
        case "UNAVAILABLE":
        case "NOT CONNECTED":
            element.innerHTML = "🔴 " + status;
            element.classList.add("stopped");
            break;

        case "NOT CONFIGURED":
            element.innerHTML = "⚪ Not Configured";
            element.classList.add("unknown");
            break;

        default:
            element.innerHTML = status || "Unknown";
            element.classList.add("unknown");

    }

}

// ========================================
// Load Dashboard
// ========================================

async function loadDashboard() {

    try {

        const response = await fetch("/api/dashboard");

        const data = await response.json();

        loadPlatformSummary(data);

        loadInfrastructure(data);

        loadDeploymentHistory(data);

    } catch (error) {

        console.error("Dashboard Error:", error);

    }

}

// ========================================
// Platform Summary
// ========================================

function loadPlatformSummary(data) {

    // Platform

    updateStatus(
        "platform-status",
        data.platform_health.status
    );

    updateText(
        "platform-health",
        data.platform_health.summary
    );

    updateText(
        "last-updated",
        new Date().toLocaleTimeString()
    );

    // Azure

    updateStatus(
        "azure-status",
        data.infrastructure.azure
    );

    updateText(
        "azure-region",
        "Central India"
    );

    // AKS

    updateStatus(
        "aks-status",
        data.infrastructure.aks.status
    );

    updateText(
        "node-count",
        data.kubernetes.nodes.total
    );

    updateText(
        "pod-count",
        data.kubernetes.pods.total
    );

    updateText(
        "aks-version",
        data.infrastructure.aks.version
    );

    // Applications

    updateText(
        "application-count",
        data.applications.length
    );

    const healthyApps = data.applications.filter(

        app => app.health === "Healthy"

    ).length;

    updateText(
        "healthy-applications",
        healthyApps
    );

    // GitOps

    updateText(
        "argocd-app-count",
        data.gitops.length
    );

    const healthyGitOps = data.gitops.filter(

        app => app.health === "Healthy"

    ).length;

    updateStatus(
        "argocd-status",
        healthyGitOps > 0
            ? "Healthy"
            : "Unavailable"
    );

    // Monitoring

    updateStatus(
        "monitoring-status",
        data.observability.prometheus.status
    );

    // Logging

    updateStatus(
        "logging-status",
        data.observability.loki.status
    );

    // HPA

    updateStatus(
        "hpa-status",
        data.autoscaling.active_hpas > 0
            ? "Running"
            : "Not Configured"
    );

    updateText(
        "hpa-enabled-count",
        data.autoscaling.active_hpas
    );

}

// ========================================
// Infrastructure Overview
// ========================================

function loadInfrastructure(data) {

    // Azure

    updateStatus(
        "azure-status-card",
        data.infrastructure.azure
    );

    // Azure Container Registry

    updateStatus(
        "acr-status",
        data.infrastructure.acr.status
    );

    // Terraform
    // (Later we can make this dynamic)

    updateStatus(
        "terraform-status",
        "Available"
    );

    // Docker
    // (Later we can make this dynamic)

    updateStatus(
        "docker-status",
        "Available"
    );

    // Key Vault

    updateStatus(
        "keyvault-status",
        data.infrastructure.key_vault.status
    );

    // Terraform Backend

    updateStatus(
        "backend-status",
        "Connected"
    );

}

// ========================================
// Deployment History
// ========================================

function loadDeploymentHistory(data) {

    const tbody = document.getElementById("deployment-history");

    if (!tbody) return;

    tbody.innerHTML = "";

    if (!data.deployment_history || data.deployment_history.length === 0) {

        tbody.innerHTML = `
            <tr>
                <td colspan="4">
                    No deployment history found.
                </td>
            </tr>
        `;

        return;

    }

    data.deployment_history.forEach(item => {

        const imageTag = item.Image.includes(":")
            ? item.Image.split(":").pop()
            : item.Image;

        tbody.innerHTML += `
            <tr>

                <td>${item.Application}</td>

                <td>${imageTag}</td>

                <td>${item.Status}</td>

                <td>${item.Timestamp}</td>

            </tr>
        `;

    });

}

// ========================================
// Dashboard Utilities
// ========================================

function showDashboardError(error) {

    console.error("Dashboard Error:", error);

}

// ========================================
// Refresh Dashboard
// ========================================

function refreshDashboard() {

    loadDashboard();

}

// ========================================
// Future Hooks
// ========================================

// loadPlatformJobs()
// loadPipelineStatus()
// loadPlatformEvents()
// loadResourceUsage()
// loadNotifications()
