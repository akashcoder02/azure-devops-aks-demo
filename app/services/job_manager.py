import subprocess
import threading
import os
import shlex

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

job = {
    "running": False,
    "output": ""
}


def run(command):

    if job["running"]:
        return False

    job["running"] = True
    job["output"] = ""

    def worker():

        args = shlex.split(command)

        script = os.path.join(PROJECT_ROOT, "scripts", args[0])

        process = subprocess.Popen(
            ["bash", script] + args[1:],
            cwd=PROJECT_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            job["output"] += line

        process.wait()

        job["running"] = False

    threading.Thread(target=worker, daemon=True).start()

    return True