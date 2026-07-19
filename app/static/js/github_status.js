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

    document.getElementById("workflowBadge").innerHTML = `
        ${emoji} ${data.status}<br>
        ${data.workflow}<br>
        ${data.branch}
    `;

}

refreshWorkflowStatus();

setInterval(
    refreshWorkflowStatus,
    5000
);