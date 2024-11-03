#!/bin/bash

# Define the conda environment name
CONDA_ENV_NAME="gptr"

# Check if the conda environment exists
if conda env list | grep -q "$CONDA_ENV_NAME"; then
    echo "Conda environment '$CONDA_ENV_NAME' already exists."
else
    echo "Creating conda environment '$CONDA_ENV_NAME'."
    conda create -n "$CONDA_ENV_NAME" python=3.11 -y
fi

# Activate the conda environment
source activate "$CONDA_ENV_NAME"

# Use pip to install all dependencies
echo "Installing all dependencies with pip."
pip install -r requirements.txt
pip install -r requirements-local.txt

# Ask user if they want to start the frontend
read -p "Do you want to start the frontend? (y/n): " start_frontend

if [[ $start_frontend =~ ^[Yy]$ ]]; then
    # Set START_FRONTEND to True in start_services.py
    sed -i 's/START_FRONTEND = False/START_FRONTEND = True/' start_services.py
    echo "START_FRONTEND set to True in start_services.py"

    echo "Installing npm dependencies..."
    cd frontend/nextjs
    npm install --legacy-peer-deps
    cd ../..
    echo "npm dependencies installed."
else
    # Set START_FRONTEND to False in start_services.py
    sed -i 's/START_FRONTEND = True/START_FRONTEND = False/' start_services.py
    echo "START_FRONTEND set to False in start_services.py"
fi

# Run the start_services.py script
echo "Starting services..."
trap "echo 'Terminating script...'; exit" SIGINT SIGTERM
python start_services.py "$CONDA_ENV_NAME"
