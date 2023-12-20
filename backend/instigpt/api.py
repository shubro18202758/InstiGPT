from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from instigpt.embeddings import get_embeddings
from instigpt.generator import get_chain, get_generator_model
from instigpt.retriever import get_retriever

from instigpt.input_models import ChatInput

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

embeddings = get_embeddings()
llm = get_generator_model()
retriever = get_retriever(embeddings=embeddings)
chain = get_chain(llm=llm, retriever=retriever)


@app.get("/")
async def status():
    return {"status": "up"}


@app.post("/chat")
async def chat(input: ChatInput):
    output = chain.stream(
        {
            "question": input.messages[-1].content,
            "chat_history": "\n\n".join(map(str, input.messages[:-1] or [])) or "None",
        }
    )

    return StreamingResponse(output, media_type="text/plain")
