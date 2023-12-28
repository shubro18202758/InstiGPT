from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from instigpt import llm

from . import helpers
from .input_models import ChatInput

router = APIRouter(
    dependencies=[Depends(helpers.get_user)]  # ensure all routes require authentication
)
# To use this API without authentication for testing purposes, uncomment the line below
# router = APIRouter()

embeddings = llm.get_embeddings()
model = llm.get_generator_model()
retriever = llm.get_retriever(embeddings=embeddings)
chain = llm.get_chain(llm=model, retriever=retriever)


@router.post("/chat")
async def chat(input: ChatInput):
    output = chain.stream(
        {
            "question": input.messages[-1].content
            + " according to sources of IIT Bombay",
            "chat_history": "\n\n".join(map(str, input.messages[:-1] or [])) or "None",
        },
        # Uncomment the line below to turn on debug mode
        # config=llm.generator.debug_config,
    )

    return StreamingResponse(output, media_type="text/plain")
