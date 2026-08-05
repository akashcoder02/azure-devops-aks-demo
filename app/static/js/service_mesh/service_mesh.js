/*
==========================================================
Service Mesh Navigation
==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    const tabs = document.querySelectorAll(".mesh-nav-item");

    tabs.forEach(tab => {

        tab.addEventListener("click", async () => {

            tabs.forEach(t => t.classList.remove("active"));

            tab.classList.add("active");

            await loadPage(tab.dataset.page);

        });

    });

});


async function loadPage(page) {

    const container = document.getElementById("service-mesh-content");

    let url = "";

    switch (page) {

        case "overview":
            url = "/service-mesh/page/overview";
            break;

        case "traffic":
            url = "/service-mesh/page/traffic";
            break;

        case "security":
            url = "/service-mesh/page/security";
            break;

        case "resilience":

            url = "/service-mesh/page/resilience";

            break;

        case "observability":

            container.innerHTML = `
                <div class="mesh-card">
                    <h2>Observability</h2>
                    <p>Coming Soon</p>
                </div>
            `;
            return;

        case "demo":

            container.innerHTML = `
                <div class="mesh-card">
                    <h2>Demo Lab</h2>
                    <p>Coming Soon</p>
                </div>
            `;
            return;

        default:
            return;
    }

    try {

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error("Unable to load page.");
        }

        const html = await response.text();

        container.innerHTML = html;

        if (page === "overview") {

            if (typeof loadOverview === "function") {
                loadOverview();
            }

        }

        if (page === "traffic") {

            if (typeof loadTrafficManagement === "function") {

                loadTrafficManagement();

            }


            if (typeof initializeTrafficActions === "function") {

                initializeTrafficActions();

            }

        }

        if (page === "security") {

            if (typeof initializeSecurityDashboard === "function") {

                initializeSecurityDashboard();

            }

        }

        if (page === "resilience") {

            if (typeof loadResilience === "function") {

                loadResilience();

            }

        }

    }
    catch (error) {

        console.error(error);

        container.innerHTML = `
            <div class="mesh-card">
                <h2>Error</h2>
                <p>Unable to load page.</p>
            </div>
        `;

    }

}