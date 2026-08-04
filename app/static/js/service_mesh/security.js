/*
==========================================================
Service Mesh Security
==========================================================
*/

let securityData = {};

async function initializeSecurityDashboard() {

    await loadSecurity();

}


/*
==========================================================
LOAD
==========================================================
*/

async function loadSecurity() {

    try {

        const response = await fetch(
            "/api/service-mesh/security"
        );

        securityData = await response.json();

        updateSummary();

        updateMtls();

        updatePeerAuthentication();

        updateDestinationRules();

        updateAuthorizationPolicies();

        updateJwt();

        updateWorkloadMatrix();

        updateSidecars();

        updateCertificates();

        updateNamespaces();

        updateValidation();

        updateEvents();

    }

    catch (error) {

        console.error(error);

    }

}


/*
==========================================================
HELPER
==========================================================
*/

function setText(id, value) {

    const element = document.getElementById(id);

    if (element) {

        element.textContent = value;

    }

}

/*
==========================================================
SUMMARY
==========================================================
*/

function updateSummary() {

    if (!securityData.summary) {

        return;

    }

    setText(
        "security-last-updated",
        securityData.summary.last_updated
    );

    setText(
        "mtls-mode",
        securityData.summary.mtls
    );

    setText(
        "authorization-count",
        securityData.summary.authorization_policies
    );

    setText(
        "certificate-status",
        securityData.summary.certificates
    );

    setText(
        "jwt-status",
        securityData.summary.jwt
    );

    setText(
        "sidecar-count",
        securityData.summary.sidecars
    );

    setText(
        "security-score",
        securityData.summary.security_score
    );

}


/*
==========================================================
MTLS
==========================================================
*/

function updateMtls() {

    if (!securityData.mtls) {

        return;

    }

    setText(
        "mtls-current-mode",
        securityData.mtls.mode
    );

    setText(
        "mtls-namespace",
        securityData.mtls.namespace
    );

    setText(
        "peer-auth-status",
        securityData.mtls.peer_authentication
    );

    setText(
        "destinationrule-tls",
        securityData.mtls.destination_rule
    );

}


/*
==========================================================
PEER AUTHENTICATION
==========================================================
*/

function updatePeerAuthentication() {

    const tbody = document.getElementById(
        "peer-authentication-body"
    );

    if (!tbody) {

        return;

    }

    tbody.innerHTML = "";

    if (!securityData.peer_authentication?.length) {

        tbody.innerHTML = `
            <tr>
                <td colspan="5">
                    No Peer Authentication Found
                </td>
            </tr>
        `;

        return;

    }

    securityData.peer_authentication.forEach(item => {

        tbody.innerHTML += `

            <tr>

                <td>${item.namespace}</td>

                <td>${item.mode}</td>

                <td>${item.status}</td>

                <td>${item.age}</td>

                <td>

                    View

                </td>

            </tr>

        `;

    });

}

/*
==========================================================
DESTINATION RULES
==========================================================
*/

function updateDestinationRules() {

    const tbody = document.getElementById(
        "destinationrule-body"
    );

    if (!tbody) return;

    tbody.innerHTML = "";

    if (!securityData.destination_rules?.length) {

        tbody.innerHTML = `
            <tr>
                <td colspan="5">
                    No Destination Rules Found
                </td>
            </tr>
        `;

        return;

    }

    securityData.destination_rules.forEach(rule => {

        tbody.innerHTML += `
            <tr>

                <td>${rule.application}</td>

                <td>${rule.host}</td>

                <td>${rule.tls_mode}</td>

                <td>${rule.traffic_policy}</td>

                <td>${rule.status}</td>

            </tr>
        `;

    });

}


/*
==========================================================
AUTHORIZATION POLICIES
==========================================================
*/

function updateAuthorizationPolicies() {

    const tbody = document.getElementById(
        "authorization-policy-body"
    );

    if (!tbody) return;

    tbody.innerHTML = "";

    if (!securityData.authorization_policies?.length) {

        tbody.innerHTML = `
            <tr>
                <td colspan="5">
                    No Authorization Policies Found
                </td>
            </tr>
        `;

        return;

    }

    securityData.authorization_policies.forEach(policy => {

        tbody.innerHTML += `
            <tr>

                <td>${policy.name}</td>

                <td>${policy.namespace}</td>

                <td>${policy.action}</td>

                <td>${policy.selector}</td>

                <td>${policy.status}</td>

            </tr>
        `;

    });

}


/*
==========================================================
JWT
==========================================================
*/

function updateJwt() {

    if (!securityData.jwt) {

        return;

    }

    setText(
        "jwt-issuer",
        securityData.jwt.issuer
    );

    setText(
        "jwt-jwks",
        securityData.jwt.jwks_uri
    );

    setText(
        "jwt-workloads",
        securityData.jwt.workloads
    );

    setText(
        "jwt-current-status",
        securityData.jwt.status
    );

}

/*
==========================================================
WORKLOAD SECURITY MATRIX
==========================================================
*/

function updateWorkloadMatrix() {

    const tbody = document.getElementById(
        "workload-security-body"
    );

    if (!tbody) return;

    tbody.innerHTML = "";

    if (!securityData.workloads?.length) {

        tbody.innerHTML = `
            <tr>
                <td colspan="7">
                    No Workloads Found
                </td>
            </tr>
        `;

        return;

    }

    securityData.workloads.forEach(workload => {

        tbody.innerHTML += `

            <tr>

                <td>${workload.application}</td>

                <td>${workload.namespace}</td>

                <td>${workload.sidecar}</td>

                <td>${workload.mtls}</td>

                <td>${workload.jwt}</td>

                <td>${workload.authorization}</td>

                <td>${workload.status}</td>

            </tr>

        `;

    });

}


/*
==========================================================
SIDECARS
==========================================================
*/

function updateSidecars() {

    const tbody = document.getElementById(
        "sidecar-status-body"
    );

    if (!tbody) return;

    tbody.innerHTML = "";

    if (!securityData.sidecars?.length) {

        tbody.innerHTML = `
            <tr>
                <td colspan="7">
                    No Sidecars Found
                </td>
            </tr>
        `;

        return;

    }

    securityData.sidecars.forEach(sidecar => {

        tbody.innerHTML += `

            <tr>

                <td>${sidecar.pod}</td>

                <td>${sidecar.namespace}</td>

                <td>${sidecar.application}</td>

                <td>${sidecar.injected}</td>

                <td>${sidecar.ready}</td>

                <td>${sidecar.version}</td>

                <td>${sidecar.status}</td>

            </tr>

        `;

    });

}


/*
==========================================================
CERTIFICATES
==========================================================
*/

function updateCertificates() {

    if (securityData.certificates_summary) {

        setText(
            "root-ca-status",
            securityData.certificates_summary.root_ca
        );

        setText(
            "certificate-count",
            securityData.certificates_summary.total
        );

        setText(
            "certificate-expiring",
            securityData.certificates_summary.expiring
        );

        setText(
            "certificate-rotation",
            securityData.certificates_summary.rotation
        );

    }

    const tbody = document.getElementById(
        "certificate-table-body"
    );

    if (!tbody) return;

    tbody.innerHTML = "";

    if (!securityData.certificates?.length) {

        tbody.innerHTML = `
            <tr>
                <td colspan="6">
                    No Certificates Found
                </td>
            </tr>
        `;

        return;

    }

    securityData.certificates.forEach(cert => {

        tbody.innerHTML += `

            <tr>

                <td>${cert.workload}</td>

                <td>${cert.name}</td>

                <td>${cert.issued}</td>

                <td>${cert.expires}</td>

                <td>${cert.days_left}</td>

                <td>${cert.status}</td>

            </tr>

        `;

    });

}

/*
==========================================================
SECURITY ACTIONS
==========================================================
*/

async function applySecurity(payload) {

    try {

        const response = await fetch(

            "/api/service-mesh/security/apply",

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify(payload)

            }

        );

        const result = await response.json();

        alert(result.message || "Workflow Triggered");

    }

    catch (error) {

        console.error(error);

        alert("Unable to trigger workflow.");

    }

}


async function destroySecurity() {

    try {

        const response = await fetch(

            "/api/service-mesh/security/destroy",

            {

                method: "POST"

            }

        );

        const result = await response.json();

        alert(result.message || "Destroy Triggered");

    }

    catch (error) {

        console.error(error);

    }

}


document.addEventListener("click", async function(event) {

    switch(event.target.id) {

        case "strict-mtls-btn":

            await applySecurity({

                mtls_mode: "STRICT",

                authorization_enabled: true,

                jwt_enabled: false

            });

            break;

        case "authorization-btn":

            await applySecurity({

                mtls_mode: "STRICT",

                authorization_enabled: true,

                jwt_enabled: false

            });

            break;

        case "jwt-btn":

            await applySecurity({

                mtls_mode: "STRICT",

                authorization_enabled: true,

                jwt_enabled: true,

                jwt_issuer: "",

                jwt_jwks_uri: ""

            });

            break;

        case "audit-btn":

            console.log("Security Audit");

            break;

        case "kiali-btn":

            window.open("/kiali", "_blank");

            break;

        default:

            break;

    }

});