// ========================================
// Azure DevOps IDP Dashboard
// ========================================

document.addEventListener("DOMContentLoaded", () => {

    loadPlatformStatus();

    loadJobStatus();

    setInterval(loadPlatformStatus, 5000);

    setInterval(loadJobStatus, 1000);

    bindButtons();
    loadApplicationStatus();

    setInterval(loadApplicationStatus, 5000);

});


// ========================================
// Button Events
// ========================================

function bindButtons() {

    document.getElementById("start-btn")
        .addEventListener("click", () => run("start"));

    document.getElementById("stop-btn")
        .addEventListener("click", () => run("stop"));

    document.getElementById("doctor-btn")
        .addEventListener("click", () => run("doctor"));

    document.getElementById("tic-deploy-btn")
        .addEventListener("click", () => runApplication("tic-tac-toe", "deploy"));

    document.getElementById("tic-status-btn")
        .addEventListener("click", () => runApplication("tic-tac-toe", "status"));

    document.getElementById("tic-undeploy-btn")
        .addEventListener("click", () => runApplication("tic-tac-toe", "undeploy"));


    document.getElementById("tic-open-btn")
        .addEventListener("click", () => {

            const url = document.getElementById("tic-open-btn").dataset.url;

            if (url) {
            window.open(url, "_blank");
            }

        });

}


// ========================================
// Execute Script
// ========================================

async function run(action) {

    const response = await fetch("/api/run", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            action: action

        })

    });

    const result = await response.json();

    if (!result.success) {

        alert("Another job is already running.");

    }

}

async function runApplication(app, action) {

    const response = await fetch(
        `/api/applications/${app}/${action}`,
        {
            method: "POST"
        }
    );

    const result = await response.json();

    if (!result.success) {

        alert("Another job is already running.");

    }

}

function updateStatus(id, status) {

    const element = document.getElementById(id);

    if (!element) return;

    element.className = "";

    const value = (status || "").trim().toUpperCase();

    switch (value) {

        case "RUNNING":
            element.innerHTML = "🟢 Running";
            element.classList.add("running");
            break;

        case "CONNECTED":
            element.innerHTML = "🟢 Connected";
            element.classList.add("running");
            break;

        case "READY":
            element.innerHTML = "🟢 Ready";
            element.classList.add("running");
            break;

        case "STOPPED":
            element.innerHTML = "🔴 Stopped";
            element.classList.add("stopped");
            break;

        case "NOT_CONNECTED":
            element.innerHTML = "🔴 Not Connected";
            element.classList.add("stopped");
            break;

        default:
            element.innerHTML = value || "Unknown";
            element.classList.add("unknown");
    }

}

// ========================================
// Platform Status
// ========================================

async function loadPlatformStatus() {

    const response = await fetch("/api/platform-status");

    const data = await response.json();

    updateStatus("azure-status", data.AZURE);

    updateStatus("terraform-status", data.TERRAFORM_STATUS);

    updateStatus("docker-status", data.DOCKER);

    updateStatus("aks-status", data.AKS);

    updateStatus("acr-status", data.ACR_STATUS);

    updateStatus("platform-status", data.AKS);

    document.getElementById("node-count").innerText =
        data.NODES || "0";

    document.getElementById("pod-count").innerText =
        data.PODS || "0";

    document.getElementById("platform-summary").innerText =
        data.CLUSTER || "Offline";

    console.log("AKS Status =", data.AKS);

    const platformRunning = (data.AKS || "").trim().toUpperCase() === "RUNNING";

    console.log("Platform Running =", platformRunning); 

    const startBtn = document.getElementById("start-btn");
    const stopBtn = document.getElementById("stop-btn");

    startBtn.disabled = platformRunning;
    stopBtn.disabled = !platformRunning;

    if (platformRunning) {

        startBtn.style.opacity = "0.4";
        startBtn.style.cursor = "not-allowed";

        stopBtn.style.opacity = "1";
        stopBtn.style.cursor = "pointer";

} else {

        startBtn.style.opacity = "1";
        startBtn.style.cursor = "pointer";

        stopBtn.style.opacity = "0.4";
        stopBtn.style.cursor = "not-allowed";

}

}

async function loadApplicationStatus() {

    const response = await fetch("/api/applications/tic-tac-toe/status");

    const data = await response.json();

    const openBtn = document.getElementById("tic-open-btn");

    const deployBtn = document.getElementById("tic-deploy-btn");
    const undeployBtn = document.getElementById("tic-undeploy-btn");
    const statusBtn = document.getElementById("tic-status-btn");

    if (data.URL && data.URL !== "-") {

        openBtn.disabled = false;

        openBtn.dataset.url = data.URL;

        document.getElementById("tic-status").innerHTML =
            "🟢 Running";

        document.getElementById("tic-summary").innerHTML =
            data.URL;

        deployBtn.disabled = true;
        undeployBtn.disabled = false;
        statusBtn.disabled = false;

        deployBtn.style.opacity = "0.4";
        deployBtn.style.cursor = "not-allowed";

        undeployBtn.style.opacity = "1";
        undeployBtn.style.cursor = "pointer";

        statusBtn.style.opacity = "1";
        statusBtn.style.cursor = "pointer";

    } else {

        openBtn.disabled = true;

        openBtn.dataset.url = "";

        document.getElementById("tic-status").innerHTML =
            "🔴 Not Deployed";

        document.getElementById("tic-summary").innerHTML =
            "Ready to deploy";
        deployBtn.disabled = false;
        undeployBtn.disabled = true;
        statusBtn.disabled = false;

        deployBtn.style.opacity = "1";
        deployBtn.style.cursor = "pointer";

        undeployBtn.style.opacity = "0.4";
        undeployBtn.style.cursor = "not-allowed";

        statusBtn.style.opacity = "1";
        statusBtn.style.cursor = "pointer";

    }

}
// ========================================
// Job Status
// ========================================

async function loadJobStatus() {

    const response = await fetch("/api/status");

    const job = await response.json();

    document.getElementById("job-status").innerText =
        job.status;

    document.getElementById("job-script").innerText =
        job.script || "None";

    document.getElementById("terminal").innerText =
        job.output || "Waiting for platform commands...";

    if (job.status === "COMPLETED") {

    loadPlatformStatus();
    loadApplicationStatus();

}

}

// ========================================
// Clock
// ========================================

function updateClock() {

    document.getElementById("clock").textContent =
        new Date().toLocaleString();

}

setInterval(updateClock, 1000);

updateClock();