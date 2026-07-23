async function install(component){

    const response = await fetch(

        `/api/install/${component}`,

        {
            method: "POST"
        }

    );

    const result = await response.json();

    alert(result.message);

}


async function uninstall(component){

    const response = await fetch(

        `/api/uninstall/${component}`,

        {
            method: "POST"
        }

    );

    const result = await response.json();

    alert(result.message);

}


if(document.getElementById("install-argocd")){

    document
        .getElementById("install-argocd")
        .addEventListener(
            "click",
            () => install("argocd")
        );

    document
        .getElementById("install-monitoring")
        .addEventListener(
            "click",
            () => install("monitoring")
        );

    document
        .getElementById("install-logging")
        .addEventListener(
            "click",
            () => install("logging")
        );

    document
        .getElementById("uninstall-argocd")
        .addEventListener(
            "click",
            () => uninstall("argocd")
        );

    document
        .getElementById("uninstall-monitoring")
        .addEventListener(
            "click",
            () => uninstall("monitoring")
        );

    document
        .getElementById("uninstall-logging")
        .addEventListener(
            "click",
            () => uninstall("logging")
        );

}

/* ----------------------------- */
/* DevSecOps                     */
/* ----------------------------- */

document
    .getElementById("install-devsecops")
    ?.addEventListener(
        "click",
        async () => {

            const response = await fetch(

                "/api/platform/install/devsecops",

                {
                    method: "POST"
                }

            );

            const data = await response.json();

            alert(data.message);

            location.reload();

        }
    );


document
    .getElementById("uninstall-devsecops")
    ?.addEventListener(
        "click",
        async () => {

            const response = await fetch(

                "/api/platform/uninstall/devsecops",

                {
                    method: "POST"
                }

            );

            const data = await response.json();

            alert(data.message);

            location.reload();

        }
    );


document
    .getElementById("status-devsecops")
    ?.addEventListener(
        "click",
        async () => {

            const response = await fetch(

                "/api/platform/status/devsecops"

            );

            const data = await response.json();

            alert(

                JSON.stringify(
                    data,
                    null,
                    4
                )

            );

        }
    );