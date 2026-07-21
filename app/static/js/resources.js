// ================================
// Azure Resource Center
// ================================

document.addEventListener("DOMContentLoaded", () => {

    console.log("Azure Resource Center Loaded");

    loadDashboard();

    bindButtons();

});


// ================================
// Buttons
// ================================

function bindButtons() {

    const refresh = document.getElementById("refreshBtn");

    const scan = document.getElementById("scanBtn");

    if (refresh) {

        refresh.onclick = () => {

            loadDashboard();

        };

    }

    if (scan) {

        scan.onclick = () => {

            triggerWorkflow();

        };

    }

}


// ================================
// Load Dashboard
// ================================

function loadDashboard() {

    loadCharts();

    loadSampleData();

}


// ================================
// Trigger GitHub Action
// ================================

async function triggerWorkflow() {

    document.getElementById("workflowStatus").innerHTML = "Running";

    try {

        const response = await fetch("/api/platform/resources", {

            method: "POST"

        });

        const data = await response.json();

        console.log(data);

        pollWorkflow();

    }

    catch (err) {

        console.error(err);

    }

}


// ================================
// Poll Workflow
// ================================

function pollWorkflow() {

    let counter = 0;

    const timer = setInterval(() => {

        counter++;

        console.log("Checking workflow...");

        // TODO

        // Replace with GitHub API

        if (counter === 5) {

            clearInterval(timer);

            document.getElementById("workflowStatus").innerHTML = "Completed";

            loadDashboard();

        }

    }, 3000);

}


// ================================
// Sample Dashboard
// ================================

function loadSampleData() {

    setValue("monthlyCost", "₹7,482");

    setValue("runningResources", "18");

    setValue("azureServices", "11");

    setValue("platformHealth", "98%");

    setValue("lastScan", "Now");

    document.getElementById("costTable").innerHTML = `

<tr>

<td>AKS</td>

<td>Healthy</td>

<td>₹180</td>

<td>₹5400</td>

<td>High</td>

</tr>

<tr>

<td>Load Balancer</td>

<td>Healthy</td>

<td>₹14</td>

<td>₹420</td>

<td>Medium</td>

</tr>

<tr>

<td>Storage</td>

<td>Healthy</td>

<td>₹12</td>

<td>₹360</td>

<td>Medium</td>

</tr>

<tr>

<td>ACR</td>

<td>Healthy</td>

<td>₹3</td>

<td>₹95</td>

<td>Low</td>

</tr>

<tr>

<td>Key Vault</td>

<td>Healthy</td>

<td>₹1</td>

<td>₹22</td>

<td>Low</td>

</tr>

`;

    document.getElementById("recommendations").innerHTML = `

<div class="mini-card">

AKS contributes most of the monthly cost.

</div>

<div class="mini-card">

Monitoring is healthy.

</div>

<div class="mini-card">

Logging stack is operational.

</div>

<div class="mini-card">

Public IP is allocated.

</div>

`;

}


// ================================
// Charts
// ================================

function loadCharts() {

    if (window.costChart) {

        window.costChart.destroy();

    }

    if (window.resourceChart) {

        window.resourceChart.destroy();

    }

    const costCtx = document.getElementById("costChart");

    window.costChart = new Chart(costCtx, {

        type: "bar",

        data: {

            labels: [

                "AKS",

                "LB",

                "Storage",

                "ACR",

                "Key Vault"

            ],

            datasets: [{

                label: "Monthly Cost",

                data: [

                    5400,

                    420,

                    360,

                    95,

                    22

                ]

            }]

        }

    });

    const resourceCtx = document.getElementById("resourceChart");

    window.resourceChart = new Chart(resourceCtx, {

        type: "doughnut",

        data: {

            labels: [

                "AKS",

                "Networking",

                "Storage",

                "Security",

                "Registry"

            ],

            datasets: [{

                data: [

                    72,

                    10,

                    8,

                    5,

                    5

                ]

            }]

        }

    });

}


// ================================
// Helpers
// ================================

function setValue(id, value) {

    const element = document.getElementById(id);

    if (element) {

        element.innerHTML = value;

    }

}