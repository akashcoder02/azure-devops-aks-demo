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

async function refreshTerminal(){

    const terminal=document.getElementById("terminal");

    const response=await fetch("/api/status");

    const data=await response.json();

    terminal.textContent=data.output;

}

setInterval(refreshTerminal,1000);

document.addEventListener("DOMContentLoaded",()=>{

    document.getElementById("doctor-btn").onclick=()=>runAction("doctor");

    document.getElementById("start-btn").onclick=()=>runAction("start");

    document.getElementById("stop-btn").onclick=()=>runAction("stop");

});