async function refreshWorkflowStatus(){

    const response =
        await fetch("/api/github/status");

    const data =
        await response.json();

    let emoji = "🟡";

    if(data.status === "completed"){

        emoji =
            data.conclusion === "success"
            ? "🟢"
            : "🔴";

    }

    if(data.status === "in_progress"){

        emoji = "🔵";

    }

    document.getElementById(
        "workflowBadge-" + data.application
    ).innerHTML = `

    <div class="workflow-card">

    <div class="status-badge">
    ${emoji} ${data.status.toUpperCase()}
    </div>

    <div class="workflow-info">

    <div>
    <strong>Workflow</strong>
    ${data.workflow}
    </div>

    <div>
    <strong>Branch</strong>
    ${data.branch}
    </div>

    <div>
    <strong>Run</strong>
    #${data.run_number}
    </div>

    <div>
    <strong>Started</strong>
    ${new Date(data.created_at).toLocaleString()}
    </div>

    <a href="${data.url}" target="_blank">

    🔗 View Workflow

    </a>

    </div>

    </div>

    `;

}

refreshWorkflowStatus();

setInterval(
    refreshWorkflowStatus,
    5000
);