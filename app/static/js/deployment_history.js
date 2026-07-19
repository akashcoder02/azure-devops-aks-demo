async function loadDeploymentHistory(){

    const response =
        await fetch("/api/deployments");

    const history =
        await response.json();

    const container =
        document.getElementById(
            "deploymentHistory"
        );

    if(!container){
        return;
    }

    container.innerHTML = "";

    history.forEach(run => {

        let icon = "🟡";

        if(run.status === "completed"){

            icon =
                run.conclusion === "success"
                ? "🟢"
                : "🔴";

        }
        else if(run.status === "in_progress"){

            icon = "🔵";

        }

        container.innerHTML += `

        <div class="history-card">

            <div class="history-left">

                <h4>${run.name}</h4>

                <small>${new Date(run.created_at).toLocaleString()}</small>

            </div>

            <div class="history-right">

                <span>${icon} ${run.status}</span>

                <br><br>

                <a href="${run.url}"
                   target="_blank">

                    View Workflow

                </a>

            </div>

        </div>

        `;

    });

}

loadDeploymentHistory();