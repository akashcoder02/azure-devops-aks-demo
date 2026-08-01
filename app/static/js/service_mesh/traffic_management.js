console.log("Traffic Management JS Loaded");

/*
==========================================================
Traffic Management
==========================================================
*/

async function loadTrafficManagement() {

    try {

        const response = await fetch("/api/service-mesh/traffic");

        if (!response.ok) {
            throw new Error("Failed to load Traffic Management.");
        }

        const data = await response.json();

        updateTrafficSummary(data);

        populateApplicationRouting(
            data.virtual_services || []
        );

        populateTrafficPolicies(
            data.destination_rules || []
        );

        populateGatewayDetails(
            data.gateways || []
        );

    }
    catch (error) {

        console.error("Traffic Management:", error);

        showTrafficError();

    }

}

/* ==========================================================
   SUMMARY
========================================================== */

function updateTrafficSummary(data) {

    const summary = data.summary || {};

    const gateways =
        summary.gateways ??
        data.gateways?.length ??
        0;

    const virtualServices =
        summary.virtual_services ??
        data.virtual_services?.length ??
        0;

    const destinationRules =
        summary.destination_rules ??
        data.destination_rules?.length ??
        0;

    const applications =
        summary.applications ??
        new Set(
            (data.virtual_services || []).map(v => v.application)
        ).size;

    const gatewayCard = document.getElementById("traffic-gateways");
    const virtualServiceCard = document.getElementById("traffic-virtual-services");
    const destinationRuleCard = document.getElementById("traffic-destination-rules");
    const applicationCard = document.getElementById("traffic-applications");

    if (gatewayCard)
        gatewayCard.textContent = gateways;

    if (virtualServiceCard)
        virtualServiceCard.textContent = virtualServices;

    if (destinationRuleCard)
        destinationRuleCard.textContent = destinationRules;

    if (applicationCard)
        applicationCard.textContent = applications;

}

/* ==========================================================
   APPLICATION ROUTING
========================================================== */

function populateApplicationRouting(virtualServices) {

    const tbody = document.getElementById("application-routing-table");

    if (!tbody) {
        return;
    }

    if (!virtualServices || virtualServices.length === 0) {

        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center">
                    No Application Routing found.
                </td>
            </tr>
        `;

        return;
    }

    tbody.innerHTML = virtualServices.map(vs => `

        <tr>

            <td>
                ${vs.application ?? "-"}
            </td>

            <td>
                ${vs.route ?? "-"}
            </td>

            <td>
                ${vs.gateway ?? "-"}
            </td>

            <td>
                ${vs.subset ?? "-"}
            </td>

            <td>
                ${vs.weight ?? "-"}%
            </td>

            <td>
                <span class="status-badge status-running">
                    ${vs.status ?? "Healthy"}
                </span>
            </td>

        </tr>

    `).join("");

}

/* ==========================================================
   TRAFFIC POLICIES
========================================================== */

function populateTrafficPolicies(destinationRules) {

    const tbody = document.getElementById("traffic-policy-table");

    if (!tbody) {
        return;
    }

    if (!destinationRules || destinationRules.length === 0) {

        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center">
                    No Traffic Policies found.
                </td>
            </tr>
        `;

        return;
    }

    tbody.innerHTML = destinationRules.map(dr => `

        <tr>

            <td>
                ${dr.application ?? "-"}
            </td>

            <td>
                ${dr.max_retries ?? "-"}
            </td>

            <td>
                ${dr.idle_timeout ?? "-"}
            </td>

            <td>
                ${dr.subset ?? "-"}
            </td>

            <td>
                ${dr.load_balancer ?? "-"}
            </td>

            <td>
                <span class="status-badge status-running">
                    ${dr.status ?? "Healthy"}
                </span>
            </td>

        </tr>

    `).join("");

}

/* ==========================================================
   TRAFFIC POLICIES
========================================================== */

function populateTrafficPolicies(destinationRules) {

    const tbody = document.getElementById("traffic-policy-table");

    if (!tbody) {
        return;
    }

    if (!destinationRules || destinationRules.length === 0) {

        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center">
                    No Traffic Policies found.
                </td>
            </tr>
        `;

        return;
    }

    tbody.innerHTML = destinationRules.map(dr => `

        <tr>

            <td>
                ${dr.application ?? "-"}
            </td>

            <td>
                ${dr.max_retries ?? "-"}
            </td>

            <td>
                ${dr.idle_timeout ?? "-"}
            </td>

            <td>
                ${dr.subset ?? "-"}
            </td>

            <td>
                ${dr.load_balancer ?? "-"}
            </td>

            <td>
                <span class="status-badge status-running">
                    ${dr.status ?? "Healthy"}
                </span>
            </td>

        </tr>

    `).join("");

}

function initializeTrafficActions() {

    console.log("Initializing Traffic Management buttons");


    document
    .getElementById("refresh-mesh-btn")
    ?.addEventListener("click", () => {

        console.log("Refresh clicked");

        loadTrafficManagement();

    });


    document
    .getElementById("gateway-status-btn")
    ?.addEventListener("click", () => {

        document
        .getElementById("gateway-details-table")
        ?.scrollIntoView({
            behavior:"smooth"
        });

    });


    document
    .getElementById("metrics-btn")
    ?.addEventListener("click", () => {

        window.open(
            "/api/monitoring",
            "_blank"
        );

    });


    document
    .getElementById("argocd-btn")
    ?.addEventListener("click", () => {

        window.open("/argocd-status","_blank");

    });


    document
    .getElementById("shift-traffic-btn")
    ?.addEventListener("click", () => {

        openTrafficOperation("Shift Traffic");

    });


    document
    .getElementById("canary-btn")
    ?.addEventListener("click", () => {

        openTrafficOperation("Canary Deployment");

    });

    document
    .getElementById("rollback-btn")
    ?.addEventListener("click", () => {

        openTrafficOperation("Rollback");

    });

    document
    .getElementById("execute-traffic-operation")
    ?.addEventListener(
        "click",
        executeTrafficOperation
    );

    document
    .getElementById("close-traffic-modal")
    ?.addEventListener(
        "click",
        closeTrafficOperation
    );

    console.log("Traffic buttons ready");

}


/* ==========================================================
   ERROR HANDLING
========================================================== */

function showTrafficError() {


    const tables = [

        "application-routing-table",

        "traffic-policy-table",

        "gateway-details-table"

    ];


    tables.forEach(tableId => {


        const tbody =
            document.getElementById(tableId);


        if (!tbody) {
            return;
        }


        tbody.innerHTML = `

            <tr>

                <td colspan="6"
                    class="text-center">

                    Unable to load Traffic Management data.

                </td>

            </tr>

        `;


    });


}




/* ==========================================================
   GATEWAY DETAILS
========================================================== */

function populateGatewayDetails(gateways) {

    const tbody = document.getElementById(
        "gateway-details-table"
    );

    if (!tbody) {
        return;
    }


    if (!gateways || gateways.length === 0) {

        tbody.innerHTML = `
            <tr>
                <td colspan="5">
                    No gateways found.
                </td>
            </tr>
        `;

        return;
    }


    tbody.innerHTML = gateways.map(gateway => `

        <tr>

            <td>
                ${gateway.name}
            </td>

            <td>
                ${gateway.hosts}
            </td>

            <td>
                ${gateway.port}
            </td>

            <td>
                ${gateway.selector}
            </td>

            <td>
                <span class="status-badge status-running">
                    ${gateway.status}
                </span>
            </td>

        </tr>

    `).join("");

}

// ==========================================================
// TRAFFIC OPERATION MODAL
// ==========================================================

let currentTrafficOperation = "";

// ==========================================================
// OPEN MODAL
// ==========================================================

function openTrafficOperation(operation) {

    currentTrafficOperation = operation;

    document.getElementById("traffic-modal-title").textContent =
        operation;

    document.getElementById("traffic-operation-modal").style.display =
        "flex";

}

// ==========================================================
// CLOSE MODAL
// ==========================================================

function closeTrafficOperation() {

    document.getElementById("traffic-operation-modal").style.display =
        "none";

}

// ==========================================================
// EXECUTE OPERATION
// ==========================================================

async function executeTrafficOperation() {

    let url = "";

    switch(currentTrafficOperation) {

        case "Shift Traffic":

            url = "/api/service-mesh/traffic-shift";

            break;

        case "Canary Deployment":

            url = "/api/service-mesh/canary";

            break;

        case "Rollback":

            url = "/api/service-mesh/rollback";

            break;

        default:

            return;

    }

    try {

        const response = await fetch(url, {

            method: "POST"

        });

        const result = await response.json();

        alert(result.message);

        closeTrafficOperation();

    }
    catch(error) {

        console.error(error);

        alert("Operation failed.");

    }

}

// ==========================================================
// TRAFFIC MANAGEMENT INITIALIZATION
// ==========================================================

function initTrafficManagementPage() {

    console.log("Traffic Management page initialized");

    loadTrafficManagement();

    initializeTrafficActions();

}