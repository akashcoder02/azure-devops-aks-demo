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

            openTrafficOperation("Rollback Traffic");

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

    document
        .getElementById("traffic-application")
        ?.addEventListener("change", function () {

            loadApplicationConfiguration(this.value);

        });

    console.log("Traffic buttons ready");

}

// ==========================================================
// TRAFFIC WEIGHT SYNCHRONIZATION
// ==========================================================

function initializeTrafficWeights() {

    const primary = document.getElementById("primary-weight");
    const canary = document.getElementById("canary-weight");

    const primaryProgress = document.getElementById("primary-progress");
    const canaryProgress = document.getElementById("canary-progress");

    const primaryText = document.getElementById("current-primary-weight");
    const canaryText = document.getElementById("current-canary-weight");

    const primarySlider = document.getElementById("primary-slider-value");
    const canarySlider = document.getElementById("canary-slider-value");

    if (
        !primary ||
        !canary ||
        !primaryProgress ||
        !canaryProgress
    ) {
        return;
    }

    function updateTraffic(primaryValue) {

        primaryValue = Math.max(0, Math.min(100, Number(primaryValue)));

        const canaryValue = 100 - primaryValue;

        primary.value = primaryValue;
        canary.value = canaryValue;

        primaryProgress.style.width = primaryValue + "%";
        canaryProgress.style.width = canaryValue + "%";

        primaryText.textContent = primaryValue + "%";
        canaryText.textContent = canaryValue + "%";

        if (primarySlider)
            primarySlider.textContent = primaryValue + "%";

        if (canarySlider)
            canarySlider.textContent = canaryValue + "%";
    }

    primary.addEventListener("input", () => {
        updateTraffic(primary.value);
    });

    canary.addEventListener("input", () => {
        updateTraffic(100 - Number(canary.value));
    });

    updateTraffic(primary.value);
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

    const applyButton =
        document.getElementById("execute-traffic-operation");

    const primaryGroup =
        document.getElementById("primary-weight").closest(".mesh-form-group");

    const canaryGroup =
        document.getElementById("canary-weight").closest(".mesh-form-group");

    

    const allocationSection =
        document.querySelector(".traffic-section:last-child");

    document.getElementById("traffic-modal-title").textContent =
        operation;

    if (operation === "Shift Traffic") {

        applyButton.textContent = "Apply Traffic";

        allocationSection.style.display = "block";

        primaryGroup.style.display = "block";
        canaryGroup.style.display = "block";

    }

    else if (operation === "Canary Deployment") {

        applyButton.textContent = "Deploy Canary";

        allocationSection.style.display = "block";

        primaryGroup.style.display = "none";

        canaryGroup.style.display = "block";

        document.getElementById("canary-weight").value = 10;

    }

    else if (operation === "Rollback Traffic") {

        applyButton.textContent = "Rollback Traffic";
        
        allocationSection.style.display = "none";

        primaryGroup.style.display = "none";

        canaryGroup.style.display = "none";

    }

    const application =
        document.getElementById("traffic-application").value;

    loadApplicationConfiguration(application);

    document.getElementById("traffic-operation-modal").style.display =
        "flex";

    initializeTrafficWeights();

}

// ==========================================================
// LOAD APPLICATION CONFIGURATION
// ==========================================================

async function loadApplicationConfiguration(application) {

    try {

        const response = await fetch(
            `/api/service-mesh/application/${application}`
        );

        if (!response.ok) {
            throw new Error("Unable to load application configuration.");
        }

        const config = await response.json();

        // ----------------------------------------
        // Application
        // ----------------------------------------

        document.getElementById("traffic-application").value =
            config.application;

        // ----------------------------------------
        // Current Configuration
        // ----------------------------------------

        document.getElementById("current-primary-version").textContent =
            config.primary.version;

        document.getElementById("current-primary-weight").textContent =
            config.primary.weight + "%";

        document.getElementById("current-canary-version").textContent =
            config.canary.version;

        document.getElementById("current-canary-weight").textContent =
            config.canary.weight + "%";

        // ----------------------------------------
        // New Configuration
        // ----------------------------------------

        document.getElementById("primary-weight").value =
            config.primary.weight;

        document.getElementById("canary-weight").value =
            config.canary.weight;

        document.getElementById("primary-slider-value").textContent =
            config.primary.weight + "%";

        document.getElementById("canary-slider-value").textContent =
            config.canary.weight + "%";

        document.getElementById("primary-progress").style.width =
            config.primary.weight + "%";

        document.getElementById("canary-progress").style.width =
            config.canary.weight + "%";

    }
    catch (error) {

        console.error(error);

        alert("Unable to load application configuration.");

    }

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

    switch (currentTrafficOperation) {

        case "Shift Traffic":

            url = "/api/service-mesh/traffic-shift";

            break;

        case "Canary Deployment":

            url = "/api/service-mesh/canary";

            break;

        case "Rollback Traffic":

            url = "/api/service-mesh/rollback";

            break;

        default:

            return;

    }

    const payload = {

        application: document.getElementById(
            "traffic-application"
        ).value,

        replicas: 1,

        service_port: 80,

        primary_version: document.getElementById(
            "current-primary-version"
        ).textContent,

        primary_weight: document.getElementById(
            "primary-weight"
        ).value,

        canary_version: document.getElementById(
            "current-canary-version"
        ).textContent,

        canary_weight: document.getElementById(
            "canary-weight"
        ).value,

        canary_enabled:
            Number(document.getElementById("canary-weight").value) > 0

    };

    try {

        const response = await fetch(url, {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify(payload)

        });

        const result = await response.json();

        showToast(
            "Traffic Operation",
            result.message
        );

        closeTrafficOperation();

    }
    catch (error) {

        console.error(error);

        showToast(
            "Operation Failed",
            "Unable to execute the traffic operation."
        );

    }

}

// ==========================================================
// TRAFFIC MANAGEMENT INITIALIZATION
// ==========================================================

function initTrafficManagementPage() {

    console.log("Traffic Management page initialized");

    loadTrafficManagement();

    initializeTrafficActions();

    console.log("Calling initializeTrafficWeights");

    initializeTrafficWeights();

}


// ==========================================================
// TOAST
// ==========================================================

function showToast(title, message) {

    const toast =
        document.getElementById("mesh-toast");

    const toastTitle =
        document.getElementById("mesh-toast-title");

    const toastMessage =
        document.getElementById("mesh-toast-message");

    if (!toast) {
        return;
    }

    toastTitle.textContent = title;

    toastMessage.textContent = message;

    toast.style.display = "block";

    setTimeout(() => {

        toast.style.display = "none";

    }, 3500);

}