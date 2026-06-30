import os
from services.script_runner import run_script

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")


def create_vm(
    vm_name,
    vm_count,
    vm_template,
    location,
    vm_size,
    admin_username,
    public_key
):
    script = os.path.join(SCRIPTS_DIR, "create-vm.sh")

    return run_script(
        script,
        [
            vm_name,
            str(vm_count),
            vm_template,
            location,
            vm_size,
            admin_username,
            public_key
        ]
)