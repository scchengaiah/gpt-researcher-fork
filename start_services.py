import subprocess
import time
import os
import sys
import psutil

def start_process(command, cwd=None):
    return subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=cwd
    )

# Start the backend server
backend_process = start_process("conda activate gptr && python -m uvicorn main:app")

# Start the frontend server
frontend_process = start_process("npm run dev", cwd="frontend/nextjs")

def terminate_process(process):
    if process.poll() is None:
        try:
            parent = psutil.Process(process.pid)
            children = parent.children(recursive=True)
            for child in children:
                child.terminate()
            parent.terminate()
            gone, alive = psutil.wait_procs(children + [parent], timeout=5)
            for p in alive:
                p.kill()
        except psutil.NoSuchProcess:
            pass

def terminate_processes():
    print("Stopping services...")
    try:
        terminate_process(backend_process)
        terminate_process(frontend_process)
        print("Services stopped.")
    except Exception as e:
        print(f"Error during termination: {e}")
    finally:
        sys.exit(0)

try:
    print("Services are running. Press CTRL+C to stop.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    terminate_processes()
except Exception as e:
    print(f"An error occurred: {e}")
    terminate_processes()