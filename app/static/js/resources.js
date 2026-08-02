// ==========================================
// Azure Resource Center
// Part 1 - Foundation
// ==========================================

let dashboardData = null;
let costChart = null;
let resourceChart = null;
let filteredResources = [];

// ==========================================
// Page Loaded
// ==========================================

document.addEventListener("DOMContentLoaded", () => {

    console.log("Azure Resource Center");

    initializeDashboard();

});

// ==========================================
// Dashboard
// ==========================================

async function initializeDashboard() {

    initializeCharts();

    document
        .getElementById("closeDrawer")
        ?.addEventListener(
            "click",
            closeResourceDrawer
        );

    document
        .getElementById("drawerOverlay")
        ?.addEventListener(
            "click",
            closeResourceDrawer
        );

    initializeInventorySearch();

    await loadAzureInventory();

    }

// ==========================================
// API
// ==========================================

async function loadAzureInventory() {

    try {

        const response = await fetch("/api/resources");

        if (!response.ok) {

            throw new Error("Unable to load Azure inventory.");

        }

        dashboardData = await response.json();

        console.log(dashboardData);

        updateKPIs();

        updateAKSCard();

        updateCharts();

        updateNetworkingCard();

        updateACRCard();

        updateKeyVaultCard();

        updateKubernetesOverview();

        updateInventoryTable();

        updateMonitoringCard();

        updateLoggingCard();

        updateGitOpsCard();

        updateApplicationsCard();

    }

    catch (error) {

        console.error(error);

        showDashboardOffline();

    }

}

// ==========================================
// KPI Cards
// ==========================================

function updateKPIs() {

    const summary = dashboardData.summary;

    setText(
        "monthlyCost",
        "N/A"
    );

    setText(
        "runningResources",
        summary.resources
    );

    setText(
        "lastScan",
        summary.last_scan
    );

    let azureServices = 0;

    const services = [

        dashboardData.azure.aks,
        dashboardData.azure.acr,
        dashboardData.azure.keyvaults,
        dashboardData.azure.public_ips

    ];

    services.forEach(service => {

        if (service.status === "healthy") {

            azureServices++;

        }

    });

    setText(
        "azureServices",
        azureServices
    );

    const sections = [

        dashboardData.azure.resources,

        dashboardData.azure.aks,

        dashboardData.azure.acr,

        dashboardData.azure.keyvaults,

        dashboardData.azure.public_ips,

        dashboardData.kubernetes.nodes,

        dashboardData.kubernetes.pods,

        dashboardData.kubernetes.deployments,

        dashboardData.kubernetes.services,

        dashboardData.kubernetes.ingresses,

        dashboardData.kubernetes.namespaces

    ];

    let healthy = 0;

    sections.forEach(section => {

        if (section.status === "healthy") {

            healthy++;

        }

    });

    setText(
        "platformHealth",
        healthy + " / " + sections.length
    );

}

// ==========================================
// AKS Card
// ==========================================

function updateAKSCard() {

    const aks = dashboardData.azure.aks;

    console.log("AKS API", aks);
    console.log("Nodes", dashboardData.kubernetes.nodes);
    console.log("Pods", dashboardData.kubernetes.pods);

    if (!dashboardData.platform.aks_available) {

        setText("aksStatus", "Offline");
        setText("aksNodes", "--");
        setText("aksPods", "--");
        setText("aksVersion", "--");

        return;

    }

    const cluster = aks.items[0];

    setText("aksStatus", "Running");

    setText(
        "aksVersion",
        cluster.kubernetesVersion || "--"
    );

    setText(
        "aksNodes",
        dashboardData.kubernetes.nodes.count
    );

    setText(
        "aksPods",
        dashboardData.kubernetes.pods.count
    );

}

// ==========================================
// Networking Card
// ==========================================

function updateNetworkingCard() {

    const network = dashboardData.azure.public_ips;

    if (network.status !== "healthy") {

        setText("networkStatus", "Offline");
        setText("publicIpCount", "--");

        return;

    }

    setText("networkStatus", "Healthy");

    setText(
        "publicIpCount",
        network.count
    );

}

// ==========================================
// Charts
// ==========================================

function initializeCharts() {

    const costCanvas = document.getElementById("costChart");
    const resourceCanvas = document.getElementById("resourceChart");

    if (costCanvas) {

        costChart = new Chart(costCanvas, {

            type: "bar",

            data: {

                labels: [],

                datasets: [{

                    label: "Resources",

                    data: []

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false

            }

        });

    }

    if (resourceCanvas) {

        resourceChart = new Chart(resourceCanvas, {

            type: "doughnut",

            data: {

                labels: [],

                datasets: [{

                    data: []

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false

            }

        });

    }

}

function updateCharts() {

    if (!dashboardData) {

        return;

    }

    if (costChart) {

        costChart.data.labels = [

            "Resources",

            "AKS",

            "ACR",

            "Key Vault",

            "Public IP"

        ];

        costChart.data.datasets[0].data = [

            dashboardData.azure.resources.count,

            dashboardData.azure.aks.count,

            dashboardData.azure.acr.count,

            dashboardData.azure.keyvaults.count,

            dashboardData.azure.public_ips.count

        ];

        costChart.update();

    }

    if (resourceChart) {

        resourceChart.data.labels = [

            "Azure",

            "Kubernetes"

        ];

        resourceChart.data.datasets[0].data = [

            dashboardData.azure.resources.count,

            dashboardData.kubernetes.nodes.count

        ];

        resourceChart.update();

    }

}

// ==========================================
// Offline
// ==========================================

function showDashboardOffline() {

    setText("runningResources", "--");

    setText("azureServices", "--");

    setText("platformHealth", "Offline");

}

// ==========================================
// Helpers
// ==========================================

function setText(id, value) {

    const element = document.getElementById(id);

    if (!element) {

        return;

    }

    element.textContent = value;

}

// ==========================================
// AKS
// ==========================================

function updateAKSCard() {

    const aks = dashboardData.azure.aks;

    if (aks.status !== "healthy") {

        setText("aksStatus", "Offline");
        return;

    }

    const cluster =
        aks.items.length > 0
        ? aks.items[0]
        : null;

    setText("aksStatus", "Running");

    setText(
        "aksVersion",
        cluster?.kubernetesVersion ?? "--"
    );

    setText(
        "aksNodes",
        dashboardData.kubernetes.nodes.count
    );

    setText(
        "aksPods",
        dashboardData.kubernetes.pods.count
    );

}

// ==========================================
// ACR Card
// ==========================================

function updateACRCard() {

    const acr = dashboardData.azure.acr;

    if (acr.status !== "healthy" || acr.count === 0) {

        setText("acrStatus", "Offline");
        setText("acrName", "--");
        setText("acrCount", "0");
        return;

    }

    const registry = acr.items[0];

    setText("acrStatus", "Healthy");

    setText(
        "acrName",
        registry.name || "--"
    );

    setText(
        "acrCount",
        acr.count
    );

}

// ==========================================
// Key Vault Card
// ==========================================

function updateKeyVaultCard() {

    const vault = dashboardData.azure.keyvaults;

    if (vault.status !== "healthy" || vault.count === 0) {

        setText("kvStatus", "Offline");
        setText("kvName", "--");
        setText("kvCount", "0");
        return;

    }

    const keyVault = vault.items[0];

    setText("kvStatus", "Healthy");

    setText(
        "kvName",
        keyVault.name || "--"
    );

    setText(
        "kvCount",
        vault.count
    );

}

// ==========================================
// Monitoring Card
// ==========================================

function updateMonitoringCard() {

    if (!dashboardData.monitoring) {

        return;

    }

    const prometheus = dashboardData.monitoring.prometheus;
    const grafana = dashboardData.monitoring.grafana;

    setText(
        "prometheusStatus",
        prometheus.count > 0 ? "Running" : "Offline"
    );

    setText(
        "grafanaStatus",
        grafana.count > 0 ? "Running" : "Offline"
    );

    setText(
        "monitoringPods",
        prometheus.count + grafana.count
    );

}

// ==========================================
// Kubernetes Overview
// ==========================================

function updateKubernetesOverview() {

    const kubernetes = dashboardData.kubernetes;

    if (!dashboardData.platform.kubernetes_connected) {

        setText("podsCount", "--");
        setText("deploymentsCount", "--");
        setText("servicesCount", "--");
        setText("ingressCount", "--");
        setText("namespacesCount", "--");
        setText("pvcCount", "--");

        return;
    }

    setText(
        "deployments",
        kubernetes.deployments.count
    );

    setText(
        "services",
        kubernetes.services.count
    );

    setText(
        "ingress",
        kubernetes.ingresses.count
    );

    setText(
        "namespaces",
        kubernetes.namespaces.count
    );

    // PVC not implemented yet

    setText(
        "pvc",
        "--"
    );

}

// ==========================================
// Azure Resource Inventory
// ==========================================

function updateInventoryTable() {

    const tbody = document.getElementById("inventoryTable");

    if (!tbody) {

        return;

    }

    tbody.innerHTML = "";

    const resources =
        filteredResources.length > 0
            ? filteredResources
            : dashboardData.azure.resources.items;

    if (!resources || resources.length === 0) {

        tbody.innerHTML = `

            <tr>

                <td colspan="5">

                    No Azure resources found.

                </td>

            </tr>

        `;

        return;

    }

    resources.forEach(resource => {

        const row = document.createElement("tr");

        row.style.cursor = "pointer";

        row.addEventListener("click", () => {

            openResourceDrawer(resource);

        });

        row.innerHTML = `

            <td>${resource.name || "--"}</td>

            <td>${formatResourceType(resource.type)}</td>

            <td>${resource.resourceGroup || "--"}</td>

            <td>${resource.location || "--"}</td>

            <td>
                <span class="success">
                    Healthy
                </span>
            </td>

        `;

        tbody.appendChild(row);

    });

}

// ==========================================
// Inventory Search
// ==========================================

function initializeInventorySearch() {

    const search = document.getElementById("inventorySearch");

    if (!search) {

        return;

    }

    search.addEventListener("input", function () {

        const value = this.value.toLowerCase().trim();

        if (value === "") {

            filteredResources = [];

            updateInventoryTable();

            return;

        }

        filteredResources =
            dashboardData.azure.resources.items.filter(resource => {

                return (

                    (resource.name || "")
                        .toLowerCase()
                        .includes(value)

                    ||

                    (resource.type || "")
                        .toLowerCase()
                        .includes(value)

                    ||

                    (resource.resourceGroup || "")
                        .toLowerCase()
                        .includes(value)

                    ||

                    (resource.location || "")
                        .toLowerCase()
                        .includes(value)

                );

            });

        updateInventoryTable();

    });

}

// ==========================================
// Resource Drawer
// ==========================================

function openResourceDrawer(resource){

    document.getElementById("drawerOverlay").classList.remove("hidden");
    document.getElementById("resourceDrawer").classList.remove("hidden");

    setText("drawerName", resource.name || "--");
    setText("drawerType", formatResourceType(resource.type));
    setText("drawerGroup", resource.resourceGroup || "--");
    setText("drawerLocation", resource.location || "--");
    setText(
        "drawerStatus",
        resource.properties?.provisioningState || "Unknown"
    );

    document.getElementById("drawerId").textContent =
        resource.id || "--";

    const tagsContainer = document.getElementById("drawerTags");

    if (tagsContainer) {

        tagsContainer.innerHTML = "";

        const tags = resource.tags || {};

        if (Object.keys(tags).length === 0) {

            tagsContainer.innerHTML =
                "<span>No Tags</span>";

        } else {

            Object.entries(tags).forEach(([key, value]) => {

                tagsContainer.innerHTML += `

                    <div class="tag-item">

                        <strong>${key}</strong>

                        <span>${value}</span>

                    </div>

                `;

            });

        }

    }

}

function closeResourceDrawer(){

    document.getElementById("drawerOverlay").classList.add("hidden");
    document.getElementById("resourceDrawer").classList.add("hidden");

}

// ==========================================
// Format Resource Type
// ==========================================

function formatResourceType(type) {

    if (!type) {

        return "--";

    }

    const mapping = {

        "Microsoft.ContainerService/managedClusters": "AKS",

        "Microsoft.ContainerRegistry/registries": "Container Registry",

        "Microsoft.KeyVault/vaults": "Key Vault",

        "Microsoft.Network/publicIPAddresses": "Public IP",

        "Microsoft.Storage/storageAccounts": "Storage Account"

    };

    return mapping[type] || type;

}

// ==========================================
// Monitoring
// ==========================================

function updateMonitoringCard() {

    const monitoring = dashboardData.monitoring;

    if (!dashboardData.platform.kubernetes_connected) {

        setText("prometheusStatus", "Offline");
        setText("grafanaStatus", "Offline");
        setText("monitoringPods", "--");

        return;
    }

    if (!monitoring) {

        return;

    }

    const prometheus = monitoring.prometheus;
    const grafana = monitoring.grafana;

    setText(
        "prometheusStatus",
        prometheus.count > 0 ? "Running" : "Offline"
    );

    setText(
        "grafanaStatus",
        grafana.count > 0 ? "Running" : "Offline"
    );

    setText(
        "monitoringPods",
        prometheus.count + grafana.count
    );

}

// ==========================================
// Logging Card
// ==========================================

function updateLoggingCard() {

    if (!dashboardData.platform.kubernetes_connected) {

        setText("prometheusStatus", "Offline");
        setText("grafanaStatus", "Offline");
        setText("monitoringPods", "--");

        return;
    }
    const loki = dashboardData.logging.loki;
    const fluentBit = dashboardData.logging.fluent_bit;

    setText(
        "lokiStatus",
        loki.count > 0 ? "Running" : "Offline"
    );

    setText(
        "fluentBitStatus",
        fluentBit.count > 0 ? "Running" : "Offline"
    );

    setText(
        "loggingPods",
        loki.count + fluentBit.count
    );

}

// ==========================================
// GitOps Card
// ==========================================

function updateGitOpsCard() {

    if (!dashboardData.platform.kubernetes_connected) {

        setText("prometheusStatus", "Offline");
        setText("grafanaStatus", "Offline");
        setText("monitoringPods", "--");

        return;
    }

    const pods = dashboardData.gitops.pods;
    const applications = dashboardData.gitops.applications;

    setText(
        "argocdStatus",
        pods.count > 0 ? "Running" : "Offline"
    );

    setText(
        "argocdApps",
        applications.count
    );

    let synced = 0;

    if (applications.items && Array.isArray(applications.items)) {

        applications.items.forEach(app => {

            if (
                app.status &&
                app.status.sync &&
                app.status.sync.status === "Synced"
            ) {
                synced++;
            }

        });

    }

    setText(
        "argocdSynced",
        synced
    );

}

// ==========================================
// Applications Card
// ==========================================

function updateApplicationsCard() {

    if (!dashboardData.applications) {
        return;
    }

    setText(
        "runningDeployments",
        dashboardData.applications.deployments.count
    );

    setText(
        "runningServices",
        dashboardData.applications.services.count
    );

    setText(
        "runningIngress",
        dashboardData.applications.ingresses.count
    );

}

