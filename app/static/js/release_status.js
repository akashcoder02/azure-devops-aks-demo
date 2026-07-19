function openReleaseStatus(){

    document
        .getElementById("releaseStatusModal")
        .style.display = "flex";

}

function closeReleaseStatus(){

    document
        .getElementById("releaseStatusModal")
        .style.display = "none";

}

async function refreshDeploymentStatus(){

    const response =
        await fetch("/api/github/status");

    const data =
        await response.json();

    updateDeploymentStatus(data);

}

function updateDeploymentStatus(data){

    document.getElementById("deploymentStatus")
        .innerHTML = getStatusBadge(data);

    document.getElementById("progressBar")
        .style.width = getProgress(data.status);

    document
        .getElementById("workflowButton")
        .href = data.url;

}

function getStatusBadge(data){

    if(data.status === "queued")
        return "🟡 Queued";

    if(data.status === "in_progress")
        return "🔵 Running";

    if(data.status === "completed"){

        if(data.conclusion === "success")
            return "🟢 Completed";

        return "🔴 Failed";

    }

    return "⚪ Unknown";

}

function getProgress(status){

    if(status === "queued")
        return "25%";

    if(status === "in_progress")
        return "65%";

    if(status === "completed")
        return "100%";

    return "0%";

}

setInterval(
    refreshDeploymentStatus,
    5000
);