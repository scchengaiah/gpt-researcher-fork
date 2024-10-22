from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

from backend.server.server import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
