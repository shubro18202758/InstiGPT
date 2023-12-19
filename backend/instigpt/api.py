from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from instigpt.embeddings import get_embeddings
from instigpt.generator import get_chain, get_generator_model
from instigpt.retriever import get_retriever

from instigpt.input_models import ChatInput

app = FastAPI()

embeddings = get_embeddings()
llm = get_generator_model()
retriever = get_retriever(embeddings=embeddings)
chain = get_chain(llm=llm, retriever=retriever)


@app.get("/")
async def status():
    return {"status": "up"}


@app.get("/chat")
async def chat(input: ChatInput):
    output = chain.stream(
        {
            "question": input.question,
            "chat_history": "\n\n".join(input.chat_history or []) or "None",
        }
    )

    return StreamingResponse(output, media_type="text/plain")
