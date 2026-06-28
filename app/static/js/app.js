async function runAction(action) {

    const terminal = document.getElementById("terminal");

    terminal.textContent = "Running " + action + "...";

    const response = await fetch("/api/run", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            action: action
        })

    });

    const data = await response.json();

    terminal.textContent = data.output;

}

document.addEventListener("DOMContentLoaded", () => {

    document.getElementById("start-btn").onclick = () => {
        runAction("start");
    };

    document.getElementById("stop-btn").onclick = () => {
        runAction("stop");
    };

    document.getElementById("doctor-btn").onclick = () => {
        runAction("doctor");
    };

});