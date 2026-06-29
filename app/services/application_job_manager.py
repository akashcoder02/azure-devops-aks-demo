import os
import shlex
import subprocess
import threading

from services.job_manager import job

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)


def run(command):

    if job["running"]:
        return False

    job["running"] = True
    job["status"] = "RUNNING"
    job["script"] = command
    job["output"] = ""

    def worker():

        try:

            args = shlex.split(command)

            script = os.path.join(PROJECT_ROOT, args[0])

            if not os.path.exists(script):
                raise FileNotFoundError(f"Script not found: {script}")

            process = subprocess.Popen(
                ["bash", os.path.basename(script)] + args[1:],
                cwd=os.path.dirname(script),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            for line in process.stdout:
                job["output"] += line

            return_code = process.wait()

            if return_code == 0:
                job["status"] = "COMPLETED"
            else:
                job["status"] = "FAILED"

        except Exception as e:

            job["status"] = "FAILED"
            job["output"] += f"\nERROR: {e}\n"

        finally:

            job["running"] = False

    threading.Thread(target=worker, daemon=True).start()

    return True
