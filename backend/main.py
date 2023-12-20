from dotenv import load_dotenv

load_dotenv()

import uvicorn

# NOTE: Do not remove this import. It is used by uvicorn to load the app
from instigpt.api import app

# Load test data
# from scripts.load_data_in_db import load_data_in_db
# from instigpt.embeddings import get_embeddings

# embeddings = get_embeddings()
# load_data_in_db(embeddings=embeddings)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", reload=True)
