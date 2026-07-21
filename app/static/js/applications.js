console.log("applications.js loaded");

const modal = document.getElementById("releaseModal");
console.log(modal);

const closeButton = document.querySelector(".close");

const releaseButtons = document.querySelectorAll(".release-btn");

const choiceCards = document.querySelectorAll(".choice-card");

const applicationSelect = document.getElementById("application");

releaseButtons.forEach(button => {

    button.addEventListener("click", () => {

        modal.style.display = "flex";

        applicationSelect.value = button.dataset.app;

    });

});

closeButton.addEventListener("click", () => {

    modal.style.display = "none";

});

window.addEventListener("click", (event) => {

    if(event.target === modal){

        modal.style.display = "none";

    }

});

choiceCards.forEach(card => {

    card.addEventListener("click", () => {

        const type = card.dataset.type;

        document.querySelectorAll(`[data-type="${type}"]`).forEach(item => {

            item.classList.remove("selected");

        });

        card.classList.add("selected");

    });

});

const releaseButton =
    document.querySelector(".modal .primary-btn");

releaseButton.addEventListener("click", async () => {
    console.log("Release button clicked");

    const payload = {

        application_name:
            applicationSelect.value,

        environment:
            document.querySelector(
                '[data-type="environment"].selected'
            ).dataset.value,

        deployment_strategy:
            document.querySelector(
                '[data-type="strategy"].selected'
            ).dataset.value,

        deployment_type:
            document.querySelector(
                '[data-type="deployment_type"].selected'
            ).dataset.value

    };

    await fetch("/api/github/context", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify(payload)

    });

    const response = await fetch(
        "/api/github/release",
        {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/json"
            },
            body: JSON.stringify(payload)
        }
    );

    const result = await response.json();

    if(result.success){

        modal.style.display = "none";

        openReleaseStatus();

        updateDeploymentStatus({

            application: payload.application_name,

            environment: payload.environment,

            strategy: payload.deployment_strategy,

            status: "queued"

        });

    }
    else{

        alert(result.message);

    }

});