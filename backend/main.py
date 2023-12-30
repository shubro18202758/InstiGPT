from dotenv import load_dotenv

load_dotenv()

import uvicorn

# NOTE: Do not remove this import. It is used by uvicorn to load the app
from instigpt.api import app
from instigpt.db import run_migrations

if __name__ == "__main__":
    run_migrations()
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", reload=True)
