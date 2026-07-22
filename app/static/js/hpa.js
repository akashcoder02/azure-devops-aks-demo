async function loadHPA() {

    const container = document.getElementById("hpaContainer");

    if (!container) {
        return;
    }

    const response = await fetch("/api/hpa");

    const hpas = await response.json();

    container.innerHTML = "";

    if (hpas.length === 0) {

        container.innerHTML = `
            <div class="application-card">
                <h3>No Horizontal Pod Autoscalers Found</h3>
            </div>
        `;

        return;
    }

    hpas.forEach(hpa => {

        container.innerHTML += `

        <div class="application-card">

            <div class="card-top">

                <h3>
                    ⚡ ${hpa.name}
                </h3>

                <span class="running">

                    ● Healthy

                </span>

            </div>

            <hr>

            <div class="app-details">

                <p>

                    <strong>Namespace</strong>

                    ${hpa.namespace}

                </p>

                <p>

                    <strong>Current Pods</strong>

                    ${hpa.current_replicas}

                </p>

                <p>

                    <strong>Desired Pods</strong>

                    ${hpa.desired_replicas}

                </p>

                <p>

                    <strong>Minimum Pods</strong>

                    ${hpa.min_replicas}

                </p>

                <p>

                    <strong>Maximum Pods</strong>

                    ${hpa.max_replicas}

                </p>

                <p>

                    <strong>CPU Target</strong>

                    ${hpa.cpu_target}%

                </p>

                <p>

                    <strong>Current CPU</strong>

                    ${hpa.current_cpu}%

                </p>

            </div>

            <div class="card-actions">

                <button
                    class="secondary-btn"
                    onclick="loadHPA()">

                    🔄 Refresh

                </button>

            </div>

        </div>

        `;

    });

}

loadHPA();

setInterval(loadHPA, 15000);