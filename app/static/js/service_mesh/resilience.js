/* ==========================================================
   SERVICE MESH RESILIENCE
   UI -> Flask -> GitHub Actions -> Terraform -> AKS/Istio
   ========================================================== */

"use strict";


/* ==========================================================
   HELPERS
   ========================================================== */

function byId(id) {
    return document.getElementById(id);
}


function setText(id, value) {
    const element = byId(id);

    if (element) {
        element.textContent =
            value === undefined || value === null
                ? "-"
                : value;
    }
}


function safeArray(value) {
    return Array.isArray(value)
        ? value
        : [];
}


function escapeHtml(value) {
    if (value === undefined || value === null) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


function inputValue(ids, fallback = "") {
    for (const id of ids) {

        const element = byId(id);

        if (
            element &&
            element.value !== undefined
        ) {
            return element.value;
        }
    }

    return fallback;
}


function checkboxValue(
    ids,
    fallback = false
) {
    for (const id of ids) {

        const element = byId(id);

        if (
            element &&
            typeof element.checked === "boolean"
        ) {
            return element.checked;
        }
    }

    return fallback;
}


function setBusy(
    button,
    busy
) {
    if (!button) {
        return;
    }

    button.disabled = busy;
}


/* ==========================================================
   OPTIONAL STATUS MESSAGE
   ========================================================== */

function showResilienceMessage(
    message,
    type = "info"
) {
    const element =
        byId("resilience-message") ||
        byId("resilience-status-message") ||
        byId("resilience-action-status");

    if (!element) {
        console.log(
            "[Resilience]",
            message
        );

        return;
    }

    element.textContent = message;
    element.dataset.status = type;
}


/* ==========================================================
   LOAD RESILIENCE
   ========================================================== */

async function loadResilience() {

    try {

        const response = await fetch(
            "/api/service-mesh/resilience",
            {
                method: "GET",
                cache: "no-store",
                headers: {
                    "Accept": "application/json"
                }
            }
        );


        if (!response.ok) {

            throw new Error(
                "Resilience API returned HTTP " +
                response.status
            );

        }


        const data =
            await response.json();


        const summary =
            data.summary || {};


        /* --------------------------------------------------
           SUMMARY
           -------------------------------------------------- */

        setText(
            "resilience-last-updated",
            summary.last_updated
        );


        setText(
            "retry-count",
            summary.retry_policies ?? 0
        );


        setText(
            "timeout-count",
            summary.timeouts ?? 0
        );


        setText(
            "cb-count",
            summary.circuit_breakers ?? 0
        );


        setText(
            "pool-count",
            summary.connection_pools ?? 0
        );


        setText(
            "outlier-count",
            summary.outlier_detection ?? 0
        );


        setText(
            "resilience-score",
            summary.resilience_score || "0%"
        );


        /* --------------------------------------------------
           TABLES
           -------------------------------------------------- */

        loadRetryPolicies(
            safeArray(
                data.retry_policies
            )
        );


        loadTimeoutPolicies(
            safeArray(
                data.timeouts
            )
        );


        loadCircuitBreakers(
            safeArray(
                data.circuit_breakers
            )
        );


        loadConnectionPools(
            safeArray(
                data.connection_pools
            )
        );


        loadOutlierDetection(
            safeArray(
                data.outlier_detection
            )
        );


        loadFaultInjection(
            safeArray(
                data.fault_injection
            )
        );


        loadChaosTests(
            safeArray(
                data.chaos_tests
            )
        );


        showResilienceMessage(
            "Resilience status refreshed.",
            "success"
        );


        return data;

    }


    catch (error) {

        console.error(
            "Failed to load resilience:",
            error
        );


        showResilienceMessage(
            "Unable to load resilience status: " +
            error.message,
            "error"
        );


        return null;

    }

}


/* ==========================================================
   RETRY
   ========================================================== */

function loadRetryPolicies(items) {

    const tbody =
        byId("retry-table");


    if (!tbody) {
        return;
    }


    tbody.innerHTML = "";


    if (items.length === 0) {

        tbody.innerHTML =
            "<tr>" +
            "<td colspan='5'>" +
            "No Retry Policies Found" +
            "</td>" +
            "</tr>";

        return;
    }


    items.forEach(item => {

        tbody.innerHTML += `

            <tr>

                <td>
                    ${escapeHtml(
                        item.application
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.attempts
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.per_try_timeout
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.retry_on
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.status
                    )}
                </td>

            </tr>

        `;

    });

}


/* ==========================================================
   TIMEOUTS
   ========================================================== */

function loadTimeoutPolicies(items) {

    const tbody =
        byId("timeout-table");


    if (!tbody) {
        return;
    }


    tbody.innerHTML = "";


    if (items.length === 0) {

        tbody.innerHTML =
            "<tr>" +
            "<td colspan='4'>" +
            "No Timeout Policies Found" +
            "</td>" +
            "</tr>";

        return;
    }


    items.forEach(item => {

        tbody.innerHTML += `

            <tr>

                <td>
                    ${escapeHtml(
                        item.application
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.timeout
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.current
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.status
                    )}
                </td>

            </tr>

        `;

    });

}


/* ==========================================================
   CIRCUIT BREAKERS
   ========================================================== */

function loadCircuitBreakers(items) {

    const tbody =
        byId("circuit-breaker-table");


    if (!tbody) {
        return;
    }


    tbody.innerHTML = "";


    if (items.length === 0) {

        tbody.innerHTML =
            "<tr>" +
            "<td colspan='5'>" +
            "No Circuit Breakers Found" +
            "</td>" +
            "</tr>";

        return;
    }


    items.forEach(item => {

        tbody.innerHTML += `

            <tr>

                <td>
                    ${escapeHtml(
                        item.application
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.max_connections
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.pending_requests
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.max_requests
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.status
                    )}
                </td>

            </tr>

        `;

    });

}

/* ==========================================================
   CONNECTION POOLS
   ========================================================== */

function loadConnectionPools(items) {

    const tbody =
        byId("connection-pool-table");


    if (!tbody) {
        return;
    }


    tbody.innerHTML = "";


    if (items.length === 0) {

        tbody.innerHTML =
            "<tr>" +
            "<td colspan='5'>" +
            "No Connection Pools Found" +
            "</td>" +
            "</tr>";

        return;
    }


    items.forEach(item => {

        tbody.innerHTML += `

            <tr>

                <td>
                    ${escapeHtml(
                        item.application
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.http_pool
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.tcp_pool
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.idle_timeout
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.status
                    )}
                </td>

            </tr>

        `;

    });

}


/* ==========================================================
   OUTLIER DETECTION
   ========================================================== */

function loadOutlierDetection(items) {

    const tbody =
        byId("outlier-table");


    if (!tbody) {
        return;
    }


    tbody.innerHTML = "";


    if (items.length === 0) {

        tbody.innerHTML =
            "<tr>" +
            "<td colspan='5'>" +
            "No Outlier Detection Found" +
            "</td>" +
            "</tr>";

        return;
    }


    items.forEach(item => {

        tbody.innerHTML += `

            <tr>

                <td>
                    ${escapeHtml(
                        item.application
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.errors
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.interval
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.ejection
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.status
                    )}
                </td>

            </tr>

        `;

    });

}


/* ==========================================================
   FAULT INJECTION
   ========================================================== */

function loadFaultInjection(items) {

    const tbody =
        byId("fault-table");


    if (!tbody) {
        return;
    }


    tbody.innerHTML = "";


    if (items.length === 0) {

        tbody.innerHTML =
            "<tr>" +
            "<td colspan='5'>" +
            "No Fault Injection Found" +
            "</td>" +
            "</tr>";

        return;
    }


    items.forEach(item => {

        tbody.innerHTML += `

            <tr>

                <td>
                    ${escapeHtml(
                        item.application
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.type
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.delay
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.abort_status
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.status
                    )}
                </td>

            </tr>

        `;

    });

}


/* ==========================================================
   CHAOS TESTS
   ========================================================== */

function loadChaosTests(items) {

    const tbody =
        byId("chaos-table");


    if (!tbody) {
        return;
    }


    tbody.innerHTML = "";


    if (items.length === 0) {

        tbody.innerHTML =
            "<tr>" +
            "<td colspan='4'>" +
            "No Chaos Tests Found" +
            "</td>" +
            "</tr>";

        return;
    }


    items.forEach(item => {

        tbody.innerHTML += `

            <tr>

                <td>
                    ${escapeHtml(
                        item.application
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.current_state
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.replicas
                    )}
                </td>

                <td>
                    ${escapeHtml(
                        item.status
                    )}
                </td>

            </tr>

        `;

    });

}


/* ==========================================================
   BUILD RESILIENCE PAYLOAD
   ========================================================== */

function buildResiliencePayload(action) {

    const payload = {
        action: action
    };


    /*
     * Support both kebab-case and snake_case IDs.
     * This keeps the JS compatible with the existing UI.
     */

    const fields = {

        retry_attempts: [
            "retry-attempts",
            "retry_attempts"
        ],

        per_try_timeout: [
            "per-try-timeout",
            "per_try_timeout"
        ],

        request_timeout: [
            "request-timeout",
            "request_timeout"
        ],

        max_connections: [
            "max-connections",
            "max_connections"
        ],

        max_requests_per_connection: [
            "max-requests-per-connection",
            "max_requests_per_connection"
        ],

        idle_timeout: [
            "idle-timeout",
            "idle_timeout"
        ],

        consecutive_errors: [
            "consecutive-errors",
            "consecutive_errors"
        ],

        outlier_interval: [
            "outlier-interval",
            "outlier_interval"
        ],

        base_ejection_time: [
            "base-ejection-time",
            "base_ejection_time"
        ],

        fault_delay: [
            "fault-delay",
            "fault_delay"
        ],

        fault_delay_percentage: [
            "fault-delay-percentage",
            "fault_delay_percentage"
        ],

        fault_abort_status: [
            "fault-abort-status",
            "fault_abort_status"
        ],

        fault_abort_percentage: [
            "fault-abort-percentage",
            "fault_abort_percentage"
        ]

    };


    Object.entries(fields).forEach(
        ([key, ids]) => {

            const value =
                inputValue(
                    ids,
                    ""
                );


            if (value !== "") {

                payload[key] =
                    value;

            }

        }
    );


    /* ------------------------------------------------------
       CHAOS ACTION
       ------------------------------------------------------ */

    const chaosAction =
        inputValue(
            [
                "chaos-action",
                "chaos_action"
            ],
            "none"
        );


    if (chaosAction !== "") {

        payload.chaos_action =
            chaosAction;

    }


    /* ------------------------------------------------------
       FAULT DELAY
       ------------------------------------------------------ */

    const delayControl =
        byId(
            "fault-delay-enabled"
        ) ||
        byId(
            "fault_delay_enabled"
        );


    if (delayControl) {

        payload.fault_delay_enabled =
            checkboxValue(
                [
                    "fault-delay-enabled",
                    "fault_delay_enabled"
                ],
                false
            );

    }


    /* ------------------------------------------------------
       FAULT ABORT
       ------------------------------------------------------ */

    const abortControl =
        byId(
            "fault-abort-enabled"
        ) ||
        byId(
            "fault_abort_enabled"
        );


    if (abortControl) {

        payload.fault_abort_enabled =
            checkboxValue(
                [
                    "fault-abort-enabled",
                    "fault_abort_enabled"
                ],
                false
            );

    }


    /* ------------------------------------------------------
       CHAOS ENABLED
       ------------------------------------------------------ */

    const chaosControl =
        byId(
            "chaos-enabled"
        ) ||
        byId(
            "chaos_enabled"
        );


    if (chaosControl) {

        payload.chaos_enabled =
            checkboxValue(
                [
                    "chaos-enabled",
                    "chaos_enabled"
                ],
                false
            );

    }


    /*
     * When the user explicitly selects the chaos action,
     * make sure chaos_enabled is true.
     */

    if (action === "chaos") {

        payload.chaos_enabled =
            true;

    }


    return payload;
}

/* ==========================================================
   APPLY RESILIENCE
   ========================================================== */

async function applyResilience(
    action,
    sourceButton = null
) {

    setBusy(
        sourceButton,
        true
    );


    const payload =
        buildResiliencePayload(
            action
        );


    console.log(
        "========== RESILIENCE REQUEST =========="
    );

    console.log(
        "Action:",
        action
    );

    console.log(
        "Payload:",
        payload
    );

    console.log(
        "========================================"
    );


    showResilienceMessage(
        "Applying " +
        action +
        " resilience configuration...",
        "loading"
    );


    try {

        const response =
            await fetch(
                "/api/service-mesh/resilience/apply",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",

                        "Accept":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            payload
                        )
                }
            );


        let data = {};

        try {

            data =
                await response.json();

        } catch (jsonError) {

            throw new Error(
                "Server returned an invalid JSON response."
            );

        }


        if (!response.ok) {

            throw new Error(
                data.message ||
                data.error ||
                "HTTP " +
                response.status
            );

        }


        console.log(
            "Resilience workflow response:",
            data
        );


        showResilienceMessage(
            "Resilience action '" +
            action +
            "' triggered successfully.",
            "success"
        );


        /*
         * GitHub Actions is asynchronous.
         * Give the workflow time to start and then
         * refresh the dashboard.
         */

        window.setTimeout(
            function() {
                loadResilience();
            },
            3000
        );


        return data;

    }


    catch (error) {

        console.error(
            "Resilience action failed:",
            error
        );


        showResilienceMessage(
            "Failed to apply " +
            action +
            ": " +
            error.message,
            "error"
        );


        return null;

    }


    finally {

        setBusy(
            sourceButton,
            false
        );

    }

}


/* ==========================================================
   RESET RESILIENCE
   ========================================================== */

async function resetResilience(
    sourceButton = null
) {

    setBusy(
        sourceButton,
        true
    );


    console.log(
        "========== RESET RESILIENCE =========="
    );


    showResilienceMessage(
        "Resetting resilience configuration...",
        "loading"
    );


    try {

        const response =
            await fetch(
                "/api/service-mesh/resilience/reset",
                {
                    method: "POST",

                    headers: {
                        "Accept":
                            "application/json"
                    }
                }
            );


        let data = {};

        try {

            data =
                await response.json();

        } catch (jsonError) {

            throw new Error(
                "Server returned an invalid JSON response."
            );

        }


        if (!response.ok) {

            throw new Error(
                data.message ||
                data.error ||
                "HTTP " +
                response.status
            );

        }


        console.log(
            "Resilience reset response:",
            data
        );


        showResilienceMessage(
            "Resilience reset workflow triggered successfully.",
            "success"
        );


        /*
         * Refresh after GitHub Actions has had
         * time to start applying the reset.
         */

        window.setTimeout(
            function() {
                loadResilience();
            },
            3000
        );


        return data;

    }


    catch (error) {

        console.error(
            "Resilience reset failed:",
            error
        );


        showResilienceMessage(
            "Failed to reset resilience: " +
            error.message,
            "error"
        );


        return null;

    }


    finally {

        setBusy(
            sourceButton,
            false
        );

    }

}


/* ==========================================================
   BUTTON EVENTS
   ========================================================== */

document.addEventListener(
    "click",
    async function(event) {

        /*
         * closest("button") allows clicks on an icon,
         * span, or other element inside the button.
         */

        const button =
            event.target.closest(
                "button"
            );


        if (!button) {
            return;
        }


        switch (button.id) {


            /* ------------------------------------------------
               RETRY
               ------------------------------------------------ */

            case "apply-retry-btn":

                await applyResilience(
                    "retry",
                    button
                );

                break;


            /* ------------------------------------------------
               TIMEOUT
               ------------------------------------------------ */

            case "update-timeout-btn":

                await applyResilience(
                    "timeout",
                    button
                );

                break;


            /* ------------------------------------------------
               CIRCUIT BREAKER
               ------------------------------------------------ */

            case "enable-cb-btn":

                await applyResilience(
                    "circuit-breaker",
                    button
                );

                break;


            /* ------------------------------------------------
               CONNECTION POOL
               ------------------------------------------------ */

            case "update-pool-btn":

                await applyResilience(
                    "connection-pool",
                    button
                );

                break;


            /* ------------------------------------------------
               OUTLIER DETECTION
               ------------------------------------------------ */

            case "enable-outlier-btn":

                await applyResilience(
                    "outlier",
                    button
                );

                break;


            /* ------------------------------------------------
               FAULT INJECTION
               ------------------------------------------------ */

            case "apply-fault-btn":

            case "enable-fault-btn":

            case "apply-fault-injection-btn":

                await applyResilience(
                    "fault",
                    button
                );

                break;


            /* ------------------------------------------------
               CHAOS TESTING
               ------------------------------------------------ */

            case "apply-chaos-btn":

            case "run-chaos-btn":

                await applyResilience(
                    "chaos",
                    button
                );

                break;


            /* ------------------------------------------------
               DEFAULT RESILIENCE
               ------------------------------------------------ */

            case "apply-default-resilience-btn":

                await applyResilience(
                    "defaults",
                    button
                );

                break;


            /* ------------------------------------------------
               RESET
               ------------------------------------------------ */

            case "reset-resilience-btn":

                await resetResilience(
                    button
                );

                break;


            /* ------------------------------------------------
               REFRESH
               ------------------------------------------------ */

            case "refresh-resilience-btn":

                await loadResilience();

                break;


            default:

                break;

        }

    }
);

/* ==========================================================
   INITIAL LOAD
   ========================================================== */

document.addEventListener(
    "DOMContentLoaded",
    function() {

        loadResilience();

    }
);


/* ==========================================================
   GLOBAL COMPATIBILITY
   ========================================================== */

/*
 * Keep these functions globally available.
 *
 * This preserves compatibility with:
 * - resilience.html
 * - inline onclick handlers
 * - other Service Mesh JavaScript files
 */

window.loadResilience =
    loadResilience;


window.applyResilience =
    applyResilience;


window.resetResilience =
    resetResilience;


/* ==========================================================
   END OF SERVICE MESH RESILIENCE JS
   ========================================================== */