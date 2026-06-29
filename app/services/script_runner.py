import subprocess
import os
import shlex

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)


def run_script(command):

    args = shlex.split(command)

    script_path = os.path.join(PROJECT_ROOT, args[0])

    if not os.path.exists(script_path):
        script_path = os.path.join(PROJECT_ROOT, "scripts", args[0])

    result = subprocess.run(
        ["bash", os.path.basename(script_path)] + args[1:],
        cwd=os.path.dirname(script_path),
        capture_output=True,
        text=True
    )

    return result.stdout + result.stderr