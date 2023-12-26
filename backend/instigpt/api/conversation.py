from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from instigpt.llm import get_embeddings, get_chain, get_generator_model, get_retriever

from . import helpers
from .input_models import ChatInput

from langchain_google_genai import GoogleGenerativeAIEmbeddings

router = APIRouter(
    dependencies=[Depends(helpers.get_user)]  # ensure all routes require authentication
)
# To use this API without authentication for testing purposes, uncomment the line below
# router = APIRouter()

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
# embeddings = get_embeddings()
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
    # debugging retriever:
    # docs = retriever.get_relevant_documents(input.messages[-1].content
    #         + " according to sources of IIT Bombay")
    # i = 1
    # for doc in docs:
    #     print(f"{i}> {doc}\n")
    #     i+=1

    return StreamingResponse(output, media_type="text/plain")
