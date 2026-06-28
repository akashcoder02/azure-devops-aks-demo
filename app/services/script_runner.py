import subprocess
import os


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)


def run_script(script_name):

    result = subprocess.run(
        ["bash", f"scripts/{script_name}"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )

    return result.stdout + result.stderr