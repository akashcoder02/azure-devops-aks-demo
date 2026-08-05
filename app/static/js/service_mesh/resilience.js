/*
==========================================================
LOAD RESILIENCE
==========================================================
*/

async function loadResilience() {

    try {

        const response = await fetch(
            "/api/service-mesh/resilience"
        );

        const data = await response.json();

        document.getElementById("resilience-last-updated").textContent =
            data.summary.last_updated;

        document.getElementById("retry-count").textContent =
            data.summary.retry_policies;

        document.getElementById("timeout-count").textContent =
            data.summary.timeouts;

        document.getElementById("cb-count").textContent =
            data.summary.circuit_breakers;

        document.getElementById("pool-count").textContent =
            data.summary.connection_pools;

        document.getElementById("outlier-count").textContent =
            data.summary.outlier_detection;

        document.getElementById("resilience-score").textContent =
            data.summary.resilience_score;

        loadRetryPolicies(data.retry_policies);

        loadTimeoutPolicies(data.timeouts);

        loadCircuitBreakers(data.circuit_breakers);

        loadConnectionPools(data.connection_pools);

        loadOutlierDetection(data.outlier_detection);

        loadFaultInjection(data.fault_injection);

        loadChaosTests(data.chaos_tests);

    }

    catch (error) {

        console.error(error);

    }

}


/*
==========================================================
RETRY
==========================================================
*/

function loadRetryPolicies(items) {

    const tbody = document.getElementById("retry-table");

    tbody.innerHTML = "";

    if (items.length === 0) {

        tbody.innerHTML =
            "<tr><td colspan='5'>No Retry Policies Found</td></tr>";

        return;

    }

    items.forEach(item => {

        tbody.innerHTML += `

            <tr>

                <td>${item.application}</td>

                <td>${item.attempts}</td>

                <td>${item.per_try_timeout}</td>

                <td>${item.retry_on}</td>

                <td>${item.status}</td>

            </tr>

        `;

    });

}


/*
==========================================================
TIMEOUTS
==========================================================
*/

function loadTimeoutPolicies(items) {

    const tbody = document.getElementById("timeout-table");

    tbody.innerHTML = "";

    if (items.length === 0) {

        tbody.innerHTML =
            "<tr><td colspan='4'>No Timeout Policies Found</td></tr>";

        return;

    }

    items.forEach(item => {

        tbody.innerHTML += `

            <tr>

                <td>${item.application}</td>

                <td>${item.timeout}</td>

                <td>${item.current}</td>

                <td>${item.status}</td>

            </tr>

        `;

    });

}


/*
==========================================================
CIRCUIT BREAKERS
==========================================================
*/

function loadCircuitBreakers(items) {

    const tbody = document.getElementById("circuit-breaker-table");

    tbody.innerHTML = "";

    if (items.length === 0) {

        tbody.innerHTML =
            "<tr><td colspan='5'>No Circuit Breakers Found</td></tr>";

        return;

    }

    items.forEach(item => {

        tbody.innerHTML += `

            <tr>

                <td>${item.application}</td>

                <td>${item.max_connections}</td>

                <td>${item.pending_requests}</td>

                <td>${item.max_requests}</td>

                <td>${item.status}</td>

            </tr>

        `;

    });

}


/*
==========================================================
CONNECTION POOLS
==========================================================
*/

function loadConnectionPools(items) {

    const tbody = document.getElementById("connection-pool-table");

    tbody.innerHTML = "";

    if (items.length === 0) {

        tbody.innerHTML =
            "<tr><td colspan='5'>No Connection Pools Found</td></tr>";

        return;

    }

    items.forEach(item => {

        tbody.innerHTML += `

            <tr>

                <td>${item.application}</td>

                <td>${item.http_pool}</td>

                <td>${item.tcp_pool}</td>

                <td>${item.idle_timeout}</td>

                <td>${item.status}</td>

            </tr>

        `;

    });

}


/*
==========================================================
OUTLIER DETECTION
==========================================================
*/

function loadOutlierDetection(items) {

    const tbody = document.getElementById("outlier-table");

    tbody.innerHTML = "";

    if (items.length === 0) {

        tbody.innerHTML =
            "<tr><td colspan='5'>No Outlier Detection Found</td></tr>";

        return;

    }

    items.forEach(item => {

        tbody.innerHTML += `

            <tr>

                <td>${item.application}</td>

                <td>${item.errors}</td>

                <td>${item.interval}</td>

                <td>${item.ejection}</td>

                <td>${item.status}</td>

            </tr>

        `;

    });

}


/*
==========================================================
FAULT INJECTION
==========================================================
*/

function loadFaultInjection(items) {

    const tbody = document.getElementById("fault-table");

    tbody.innerHTML = "";

    if (items.length === 0) {

        tbody.innerHTML =
            "<tr><td colspan='5'>No Fault Injection Found</td></tr>";

        return;

    }

}


/*
==========================================================
CHAOS TESTS
==========================================================
*/

function loadChaosTests(items) {

    const tbody = document.getElementById("chaos-table");

    tbody.innerHTML = "";

    if (items.length === 0) {

        tbody.innerHTML =
            "<tr><td colspan='4'>No Chaos Tests Found</td></tr>";

        return;

    }

}

/*
==========================================================
RESILIENCE ACTIONS
==========================================================
*/

async function applyResilience(action) {

    const response = await fetch(
        "/api/service-mesh/resilience/apply",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                action: action
            })
        }
    );

    return await response.json();

}


async function resetResilience() {

    const response = await fetch(
        "/api/service-mesh/resilience/reset",
        {
            method: "POST"
        }
    );

    return await response.json();

}

/*
==========================================================
BUTTON EVENTS
==========================================================
*/

document.addEventListener("click", async (e) => {

    switch (e.target.id) {

        case "apply-retry-btn":
            await applyResilience("retry");
            break;

        case "update-timeout-btn":
            await applyResilience("timeout");
            break;

        case "enable-cb-btn":
            await applyResilience("circuit-breaker");
            break;

        case "update-pool-btn":
            await applyResilience("connection-pool");
            break;

        case "enable-outlier-btn":
            await applyResilience("outlier");
            break;

        case "apply-default-resilience-btn":
            await applyResilience("defaults");
            break;

        case "reset-resilience-btn":
            await resetResilience();
            break;

        case "refresh-resilience-btn":
            await loadResilience();
            break;

    }

});