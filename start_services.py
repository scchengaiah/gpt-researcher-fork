import subprocess
import time
import os
import sys
import psutil
import signal
import threading

def start_process(command, cwd=None):
    return subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=cwd,
        bufsize=1,
        universal_newlines=True,
        encoding='utf-8'
    )

def print_output(process):
    for line in iter(process.stdout.readline, ''):
        sys.stdout.write(line)
        sys.stdout.flush()
    process.stdout.close()

# Start the backend server
backend_process = start_process("conda activate gptr && python -m uvicorn main:app")

# Start the frontend server
frontend_process = start_process("npm run dev", cwd="frontend/nextjs")

processes = [backend_process, frontend_process]

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

def terminate_processes(signum, frame):
    print("\nStopping services...")
    try:
        for process in processes:
            terminate_process(process)
        print("Services stopped.")
    except Exception as e:
        print(f"Error during termination: {e}")
    finally:
        sys.exit(0)

# Set up signal handler
signal.signal(signal.SIGINT, terminate_processes)
signal.signal(signal.SIGTERM, terminate_processes)

try:
    print("Services are running. Press CTRL+C to stop.")
    
    # Start output threads
    threads = []
    for process in processes:
        thread = threading.Thread(target=print_output, args=(process,), daemon=True)
        thread.start()
        threads.append(thread)
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

except Exception as e:
    print(f"An error occurred: {e}")
    terminate_processes(None, None)
