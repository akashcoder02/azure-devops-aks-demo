/*
==========================================================
Service Mesh Overview
==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    loadOverview();

});


async function loadOverview() {

    try {

        const response = await fetch("/api/service-mesh/overview");

        if (!response.ok) {
            throw new Error("Unable to load Service Mesh overview.");
        }

        const data = await response.json();

        updateSummaryCards(data);

        updateComponentStatus(data);

    }
    catch (error) {

        console.error(error);

        showOverviewError();

    }

}


function updateSummaryCards(data) {

    document.getElementById("mesh-version").textContent =
        data.version ?? "--";

    document.getElementById("mesh-health").textContent =
        data.health ?? "--";

    document.getElementById("mesh-gateways").textContent =
        data.gateways ?? "--";

    document.getElementById("mesh-virtualservices").textContent =
        data.virtual_services ?? "--";

    document.getElementById("mesh-destinationrules").textContent =
        data.destination_rules ?? "--";

    document.getElementById("mesh-applications").textContent =
        data.applications ?? "--";

}


function updateComponentStatus(data) {

    const tbody = document.getElementById("mesh-status-body");

    if (!tbody) {
        return;
    }

    tbody.innerHTML = "";

    (data.components || []).forEach(component => {

        tbody.innerHTML += `

        <tr>

            <td>${component.name}</td>

            <td>${component.namespace}</td>

            <td class="${getStatusClass(component.status)}">

                ${component.status}

            </td>

        </tr>

        `;

    });

}


function getStatusClass(status) {

    switch ((status || "").toLowerCase()) {

        case "running":
        case "healthy":
            return "status-running";

        case "warning":
            return "status-warning";

        case "failed":
        case "error":
            return "status-error";

        default:
            return "";

    }

}


function showOverviewError() {

    const tbody = document.getElementById("mesh-status-body");

    if (tbody) {

        tbody.innerHTML = `

        <tr>

            <td colspan="3">

                Unable to load Service Mesh information.

            </td>

        </tr>

        `;

    }

}
