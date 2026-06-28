
async function runAction(action){

    await fetch("/api/run",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            action:action
        })

    });

}

async function refreshPlatformStatus(){

    const response = await fetch("/api/platform-status");

    const data = await response.json();

    updateStatus("docker-status", data.DOCKER);
    updateStatus("aks-status", data.AKS);
    updateStatus("azure-status", data.AZURE);
    updateStatus("terraform-status", data.TERRAFORM_STATUS);
    updateStatus("acr-status", data.ACR_STATUS);
    document.getElementById("node-count").textContent = data.NODES;

    document.getElementById("pod-count").textContent = data.PODS;

    if(data.AKS==="RUNNING"){

    updateStatus("platform-status","RUNNING");

    document.getElementById("platform-summary").textContent =
        data.NODES + " Nodes • " + data.PODS + " Pods";

}
else{

    updateStatus("platform-status","STOPPED");

    document.getElementById("platform-summary").textContent =
        "Infrastructure Offline";

}

}

function updateStatus(id,status){

    const element=document.getElementById(id);

    element.className="";

    switch(status){

        case "RUNNING":

            element.innerHTML="🟢 Running";

            element.classList.add("running");

            break;

        case "CONNECTED":

            element.innerHTML="🟢 Connected";

            element.classList.add("running");

            break;

        case "READY":

            element.innerHTML="🟢 Ready";

            element.classList.add("running");

            break;

        case "STOPPED":

            element.innerHTML="🔴 Stopped";

            element.classList.add("stopped");

            break;

        case "NOT_CONNECTED":

            element.innerHTML="🔴 Not Connected";

            element.classList.add("stopped");

            break;

        case "NOT_INITIALIZED":

            element.innerHTML="🟡 Not Initialized";

            element.classList.add("warning");

            break;

        default:

            element.innerHTML="⚪ "+status;

            element.classList.add("unknown");

    }

}

async function refreshTerminal(){

    const terminal=document.getElementById("terminal");

    const response=await fetch("/api/status");

    const data=await response.json();

    terminal.textContent=data.output;

    document.getElementById("job-status").textContent = data.status;

    document.getElementById("job-script").textContent = data.script || "None";

}

function updateClock(){

    document.getElementById("clock").textContent =
        new Date().toLocaleString();

}

setInterval(updateClock,1000);

updateClock();

setInterval(refreshTerminal,1000);

setInterval(refreshPlatformStatus,5000);

refreshPlatformStatus();

refreshTerminal();

document.addEventListener("DOMContentLoaded",()=>{

    document.getElementById("doctor-btn").onclick=()=>runAction("doctor");

    document.getElementById("start-btn").onclick=()=>runAction("start");

    document.getElementById("stop-btn").onclick=()=>runAction("stop");

});