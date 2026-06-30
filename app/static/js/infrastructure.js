document
    .getElementById("provision-btn")
    .addEventListener("click", provisionVM);

async function provisionVM() {

    const payload = {

        vm_name: document.getElementById("vm-name").value,

        vm_count: parseInt(
            document.getElementById("vm-count").value

        
),

        vm_size: document.getElementById("vm-size").value,

        admin_username: document.getElementById("admin-username").value,

        vm_template: document.getElementById("vm-template").value,

        public_key: document.getElementById("public-key").value,

        location: document.getElementById("location").value

    };
    console.log(payload);
    const response = await fetch(
        "/api/infrastructure/vm",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(payload)
        }
    );

    const result = await response.json();

        console.log(result);

        alert(result.message);

}