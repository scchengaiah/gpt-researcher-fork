# GPTResearcher

## Setup - Standalone Static Frontend

Create conda environment

```bash
conda create --prefix D:/tmp/genai/venv/gptr python=3.11
```

Activate conda environment

```bash
conda activate gptr
```

CD to the cloned `gpt-researcher` repository

```bash
cd D:/github/gpt-researcher-fork
```

Install required dependencies.

```bash
pip install -r requirements.txt
```

Start the server

```bash
python -m uvicorn main:app
```

## Setup - Running NextJS Frontend via CLI

Make sure that the steps defined in the [Setup - Standalone Static Frontend](#setup---standalone-static-frontend) are completed.



## Setup Docker

Rename `.env.example` file to `.env` and update the appropriate values for the environment variables.

Execute the below docker command. This shall build the project and start the container.

```bash
docker compose up --build
```

Access the application at `http://localhost:8000` or `http://<WSL_IP_ADDRESS>:8000`