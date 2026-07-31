/*
==========================================================
Traffic Management
==========================================================
*/

async function loadTrafficManagement() {

    try {

        const response = await fetch("/api/service-mesh/traffic");

        if (!response.ok) {
            throw new Error("Unable to load Traffic Management data.");
        }

        const data = await response.json();

        updateTrafficSummary(data);

        populateTrafficTable(
            "gateway-table",
            data.gateways
        );

        populateTrafficTable(
            "virtual-service-table",
            data.virtual_services
        );

        populateTrafficTable(
            "destination-rule-table",
            data.destination_rules
        );

    }
    catch (error) {

        console.error(error);

        showTrafficError();

    }

}


/* ==========================================================
   SUMMARY
========================================================== */

function updateTrafficSummary(data) {

    document.getElementById("traffic-gateways").textContent =
        data.gateways?.length ?? 0;

    document.getElementById("traffic-virtual-services").textContent =
        data.virtual_services?.length ?? 0;

    document.getElementById("traffic-destination-rules").textContent =
        data.destination_rules?.length ?? 0;

}


/* ==========================================================
   TABLE
========================================================== */

function populateTrafficTable(tableId, resources) {

    const tbody = document.getElementById(tableId);

    if (!tbody) {
        return;
    }

    if (!resources || resources.length === 0) {

        tbody.innerHTML = `
            <tr>
                <td colspan="2">
                    No resources found.
                </td>
            </tr>
        `;

        return;

    }

    tbody.innerHTML = resources.map(resource => `

        <tr>

            <td>${resource.name}</td>

            <td>${resource.namespace}</td>

        </tr>

    `).join("");

}


/* ==========================================================
   ERROR
========================================================== */

function showTrafficError() {

    [
        "gateway-table",
        "virtual-service-table",
        "destination-rule-table"
    ].forEach(tableId => {

        const tbody = document.getElementById(tableId);

        if (!tbody) {
            return;
        }

        tbody.innerHTML = `
            <tr>
                <td colspan="2">
                    Unable to load data.
                </td>
            </tr>
        `;

    });

}