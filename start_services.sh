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

# Run the start_services.py script
echo "Starting services..."
trap "echo 'Terminating script...'; exit" SIGINT SIGTERM
python start_services.py "$CONDA_ENV_NAME"
