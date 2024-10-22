- [GPTResearcher](#gptresearcher)
  - [Setup - Standalone Static Frontend](#setup---standalone-static-frontend)
  - [Setup - Running NextJS Frontend via CLI](#setup---running-nextjs-frontend-via-cli)
    - [Prerequisites](#prerequisites)
    - [Setup and Running](#setup-and-running)
  - [Running Backend and Frontend Together](#running-backend-and-frontend-together)
    - [Prerequisites](#prerequisites-1)
    - [Running the Script](#running-the-script)
  - [Setup Docker](#setup-docker)


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

A more robust solution with enhanced features and performance.

### Prerequisites

- Node.js (v18.17.0 recommended)
- npm

### Setup and Running

1. Navigate to the NextJS directory:

    ```bash
    cd frontend/nextjs
    ```

2. Set up Node.js:

    ```bash
    nvm install 18.17.0
    nvm use 18.17.0
    ```

3. Install dependencies:

    ```bash
    npm install --legacy-peer-deps
    ```

    This command installs dependencies while ignoring peer dependency conflicts.

4. Start the development server:

    ```bash
    npm run dev
    ```

5. Access the application at `http://localhost:3000`

Note: Requires the backend server to be running on `localhost:8000` as detailed in the standalone static frontend setup.

## Running Backend and Frontend Together

You can use the provided Python script to start both the backend and frontend services together.

### Prerequisites

- Ensure all dependencies for both backend and frontend are installed as per the above instructions.

### Running the Script

1. Navigate to the directory containing `start_services.py`.

2. Run the script:

    ```bash
    python start_services.py
    ```

3. The services will start, and you can access the application at `http://localhost:3000`.

4. To stop the services, press `CTRL+C`. Note that in normal command line terminal and VS code terminal the main program can be terminated. If we use Windows latest terminal this is not working. Use VS code terminal if you want to preserve the UTF-8 content formatting.

## Setup Docker

Rename `.env.example` file to `.env` and update the appropriate values for the environment variables.

Execute the below docker command. This shall build the project and start the container.

```bash
docker compose up --build
```

Access the application at `http://localhost:8000` or `http://<WSL_IP_ADDRESS>:8000`
