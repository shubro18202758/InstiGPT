from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import auth, conversation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(conversation.router)


@app.get("/")
async def status():
    return {"status": "up"}
