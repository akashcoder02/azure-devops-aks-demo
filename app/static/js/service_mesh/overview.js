/*
==========================================================
Service Mesh Overview
==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    registerActions();
    loadOverview();

});


/* ==========================================================
   Overview
========================================================== */

async function loadOverview() {

    try {

        const response = await fetch("/api/service-mesh/overview");

        if (!response.ok) {
            throw new Error("Unable to load Service Mesh overview.");
        }

        const data = await response.json();

        updateSummaryCards(data);
        updateComponentStatus(data);
        updateLastUpdated(data);

    }
    catch (error) {

        console.error(error);
        showOverviewError();

    }

}


/* ==========================================================
   Summary Cards
========================================================== */

function updateSummaryCards(data) {


    const elements = {

        "mesh-version": data.version ?? "Not Installed",

        "mesh-health": data.health ?? "Not Installed",

        "mesh-gateways": data.gateways ?? 0,

        "mesh-virtualservices": data.virtual_services ?? 0,

        "mesh-destinationrules": data.destination_rules ?? 0,

        "mesh-applications": data.applications ?? 0,

        "gateway-count": data.gateways ?? 0,

        "virtualservice-count": data.virtual_services ?? 0,

        "destinationrule-count": data.destination_rules ?? 0,

        "application-count": data.applications ?? 0

    };


    Object.entries(elements).forEach(([id, value]) => {

        const element = document.getElementById(id);

        if (element) {

            element.textContent = value;

        }

    });

}


/* ==========================================================
   Component Status
========================================================== */

function updateComponentStatus(data) {

    const tbody = document.getElementById("mesh-status-body");

    if (!tbody) {
        return;
    }

    tbody.innerHTML = "";

    const components = data.components || [];

    if (components.length === 0) {

        tbody.innerHTML = `
            <tr>
                <td colspan="3">
                    No Service Mesh components found.
                </td>
            </tr>
        `;

        return;
    }

    components.forEach(component => {

        tbody.innerHTML += `
            <tr>
                <td>${component.name}</td>
                <td>${component.namespace}</td>
                <td>
                    <span class="${getStatusClass(component.status)}">
                        ${component.status}
                    </span>
                </td>
            </tr>
        `;

    });

}


/* ==========================================================
   Status Badge
========================================================== */

function getStatusClass(status) {

    switch ((status || "").toLowerCase()) {

        case "healthy":
        case "running":
            return "status-running";

        case "warning":
            return "status-warning";

        case "failed":
        case "error":
            return "status-error";

        case "not installed":
        case "not found":
        default:
            return "status-notfound";

    }

}


/* ==========================================================
   Last Updated
========================================================== */

function updateLastUpdated(data) {

    const element = document.getElementById("mesh-last-updated");

    if (!element) {
        return;
    }

    element.textContent = data.last_updated ?? "--";

}


/* ==========================================================
   Actions
========================================================== */

function registerActions() {

    // -------------------------
    // Summary Cards
    // -------------------------

    document.getElementById("gateway-card")?.addEventListener("click", () => {
        loadTrafficManagement();
    });

    document.getElementById("virtualservice-card")?.addEventListener("click", () => {
        loadTrafficManagement();
    });

    document.getElementById("destinationrule-card")?.addEventListener("click", () => {
        loadTrafficManagement();
    });

    document.getElementById("applications-card")?.addEventListener("click", () => {
        window.location.href = "/applications";
    });

    // -------------------------
    // Quick Actions
    // -------------------------

    document.getElementById("install-mesh-btn")?.addEventListener("click", installServiceMesh);

    document.getElementById("destroy-mesh-btn")?.addEventListener("click", destroyServiceMesh);

    document.getElementById("upgrade-mesh-btn")?.addEventListener("click", () => {
        alert("Upgrade workflow will be implemented in the next phase.");
    });

    document.getElementById("configure-mesh-btn")?.addEventListener("click", () => {
        window.location.href = "/service-mesh/traffic";
    });

    document.getElementById("demo-mesh-btn")?.addEventListener("click", () => {
        window.location.href = "/service-mesh/demo";
    });

}


/* ==========================================================
   Install
========================================================== */

async function installServiceMesh() {

    try {

        const response = await fetch("/api/service-mesh/install", {
            method: "POST"
        });

        if (!response.ok) {
            throw new Error("Installation request failed.");
        }

        const result = await response.json();

        alert(result.message);

        startStatusPolling();

    }
    catch (error) {

        console.error(error);

        alert(error.message);

    }

}


/* ==========================================================
   Destroy
========================================================== */

async function destroyServiceMesh() {

    if (!confirm("Destroy the Service Mesh?")) {
        return;
    }

    try {

        const response = await fetch("/api/service-mesh/destroy", {
            method: "POST"
        });

        if (!response.ok) {
            throw new Error("Destroy request failed.");
        }

        const result = await response.json();

        alert(result.message);

        startStatusPolling();

    }
    catch (error) {

        console.error(error);

        alert(error.message);

    }

}


/* ==========================================================
   Polling
========================================================== */

function startStatusPolling() {

    let attempts = 0;

    const maxAttempts = 60;

    const interval = setInterval(async () => {

        attempts++;

        try {

            const response = await fetch("/api/service-mesh/status");

            if (!response.ok) {
                return;
            }

            const data = await response.json();

            if (
                data.health === "Healthy" ||
                data.health === "Not Installed"
            ) {

                clearInterval(interval);

                await loadOverview();

                return;

            }

            if (attempts >= maxAttempts) {

                clearInterval(interval);

                console.warn("Status polling timed out.");

            }

        }
        catch (error) {

            console.error(error);

        }

    }, 10000);

}


/* ==========================================================
   Error
========================================================== */

function showOverviewError() {

    const tbody = document.getElementById("mesh-status-body");

    if (!tbody) {
        return;
    }

    tbody.innerHTML = `
        <tr>
            <td colspan="3">
                Unable to load Service Mesh information.
            </td>
        </tr>
    `;

}