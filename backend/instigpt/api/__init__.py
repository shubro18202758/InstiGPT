from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from instigpt import config
from . import auth, conversation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(conversation.router)


@app.get("/")
async def status():
    return {"status": "up"}
