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

    setValue("workflowStatus","Running");

    showOverlay("Triggering GitHub Action...");

    try {

        const response = await fetch("/api/resources/run", {

            method: "POST"

        });

        const data = await response.json();
        console.log("Workflow Response:", data);

        if (response.ok) {

            pollWorkflow();

        }
        else {

            hideOverlay();

            alert(data.message || "Unable to start workflow.");

        }

    }

    catch (err) {

        console.error(err);

        hideOverlay();

        setValue("workflowStatus","Failed");

    }

}


// ================================
// Poll Workflow
// ================================

function pollWorkflow() {

    let counter = 0;

    const steps = [

        "Authenticating Azure...",

        "Checking AKS...",

        "Checking Networking...",

        "Collecting Azure Resources...",

        "Calculating Cost..."

    ];

    const timer = setInterval(() => {

        counter++;

        if(counter <= steps.length){

            showOverlay(steps[counter-1]);

        }

        console.log("Checking workflow...");

        if (counter === 5) {

            clearInterval(timer);

            setValue("workflowStatus","Completed");

            hideOverlay();

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

    document.getElementById("costBreakdown").innerHTML = `

    <div class="cost-card">

    <div class="cost-top">

    <h3>AKS Cluster</h3>

    <strong>₹5,400 / month</strong>

    </div>

    <div class="cost-progress">

    <div class="cost-fill"
    style="width:72%"></div>

    </div>

    <div class="cost-bottom">

    <span>₹180/day</span>

    <span class="danger">

    High Impact

    </span>

    </div>

    </div>

    <div class="cost-card">

    <div class="cost-top">

    <h3>Load Balancer</h3>

    <strong>₹420 / month</strong>

    </div>

    <div class="cost-progress">

    <div class="cost-fill"
    style="width:18%"></div>

    </div>

    <div class="cost-bottom">

    <span>₹14/day</span>

    <span class="warning">

    Medium

    </span>

    </div>

    </div>

    <div class="cost-card">

    <div class="cost-top">

    <h3>Managed Disk</h3>

    <strong>₹360 / month</strong>

    </div>

    <div class="cost-progress">

    <div class="cost-fill"
    style="width:12%"></div>

    </div>

    <div class="cost-bottom">

    <span>₹12/day</span>

    <span class="warning">

    Medium

    </span>

    </div>

    </div>

    <div class="cost-card">

    <div class="cost-top">

    <h3>Azure Container Registry</h3>

    <strong>₹95 / month</strong>

    </div>

    <div class="cost-progress">

    <div class="cost-fill"
    style="width:5%"></div>

    </div>

    <div class="cost-bottom">

    <span>₹3/day</span>

    <span class="success">

    Low

    </span>

    </div>

    </div>

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

        },
        options:{

            responsive:true,

            maintainAspectRatio:false

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

        },
        options:{

            responsive:true,

            maintainAspectRatio:false

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

function showOverlay(message){

    const overlay = document.getElementById("scanOverlay");
    const status = document.getElementById("scanStatus");

    if (overlay && status){

        overlay.classList.remove("hidden");
        status.innerHTML = message;

    }

}

function hideOverlay(){

    const overlay = document.getElementById("scanOverlay");

    if (overlay){

        overlay.classList.add("hidden");

    }

}