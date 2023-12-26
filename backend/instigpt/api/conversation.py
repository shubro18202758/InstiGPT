from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from instigpt.llm import get_embeddings, get_chain, get_generator_model, get_retriever

from . import helpers
from .input_models import ChatInput

router = APIRouter(
    dependencies=[Depends(helpers.get_user)]  # ensure all routes require authentication
)
# To use this API wihtout authentication for testing purposes, uncomment the line below
# router = APIRouter()

embeddings = get_embeddings()
llm = get_generator_model()
retriever = get_retriever(embeddings=embeddings)
chain = get_chain(llm=llm, retriever=retriever)


@router.post("/chat")
async def chat(input: ChatInput):
    output = chain.stream(
        {
            "question": input.messages[-1].content
            + " according to sources of IIT Bombay",
            "chat_history": "\n\n".join(map(str, input.messages[:-1] or [])) or "None",
        }
    )

    return StreamingResponse(output, media_type="text/plain")
