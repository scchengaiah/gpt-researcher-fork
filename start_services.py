import subprocess
import time
import os
import sys
import psutil
import signal
import threading
import shutil
import socket
import argparse

# Configuration
BACKEND_PORT = 8000  # Default port for uvicorn
FRONTEND_PORT = 3000  # Default port for Next.js
START_FRONTEND = True  # Set to False if you don't want to start the frontend

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"  # Fallback to localhost if unable to determine IP

def start_process(command, cwd=None):
    print(f"Starting process with command: {command}")
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

def print_output(process, name):
    print(f"Starting to read output for {name}")
    try:
        for line in iter(process.stdout.readline, ''):
            sys.stdout.write(f"{name}: {line}")
            sys.stdout.flush()
    except Exception as e:
        print(f"Error reading output from {name}: {e}")
    finally:
        print(f"Finished reading output for {name}")
        process.stdout.close()

def get_backend_command(conda_env_name):
    if shutil.which('conda'):
        return f"conda run --no-capture-output -n {conda_env_name} python -m uvicorn main:app --host 0.0.0.0 --port {BACKEND_PORT}"
    else:
        print("Warning: conda not found. Trying to run without conda activation.")
        return f"python -m uvicorn main:app --host 0.0.0.0 --port {BACKEND_PORT}"

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
        for _, process in processes:
            terminate_process(process)
        print("Services stopped.")
    except Exception as e:
        print(f"Error during termination: {e}")
    finally:
        sys.exit(0)

# Set up signal handler
signal.signal(signal.SIGINT, terminate_processes)
signal.signal(signal.SIGTERM, terminate_processes)

def main():
    parser = argparse.ArgumentParser(description='Start services with specified Conda environment.')
    parser.add_argument('conda_env_name', type=str, help='Name of the Conda environment to use')
    args = parser.parse_args()

    conda_env_name = args.conda_env_name

    # Start the backend server
    backend_command = get_backend_command(conda_env_name)
    print(f"Backend command: {backend_command}")
    backend_process = start_process(backend_command)

    processes = [("Backend", backend_process)]

    # Start the frontend server if START_FRONTEND is True
    if START_FRONTEND:
        frontend_process = start_process(f"npm run dev -- -p {FRONTEND_PORT}", cwd="frontend/nextjs")
        processes.append(("Frontend", frontend_process))

    try:
        local_ip = get_local_ip()
        print("Services are running. Press CTRL+C to stop.")
        print(f"Backend service is accessible at: http://{local_ip}:{BACKEND_PORT}")
        if START_FRONTEND:
            print(f"Frontend service is accessible at: http://{local_ip}:{FRONTEND_PORT}")
        else:
            print("Frontend service is not started.")
        
        # Start output threads
        threads = []
        for name, process in processes:
            thread = threading.Thread(target=print_output, args=(process, name), daemon=True)
            thread.start()
            threads.append(thread)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    except Exception as e:
        print(f"An error occurred: {e}")
        terminate_processes(None, None)

if __name__ == "__main__":
    main()
