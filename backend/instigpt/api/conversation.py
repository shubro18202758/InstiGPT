from typing import Annotated
import uuid

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from instigpt import llm, db

from . import helpers
from .input_models import ChatInput, CreateConversationInput

router = APIRouter()

embeddings = llm.get_embeddings()
model = llm.get_generator_model()
retriever = llm.get_retriever(embeddings=embeddings)
chain = llm.get_chain(llm=model, retriever=retriever)


@router.get("/conversation")
async def get_conversations(user: Annotated[db.user.User, Depends(helpers.get_user)]):
    return db.conversation.get_conversations_of_user(user.id)


@router.post("/conversation")
async def create_conversation(
    input: CreateConversationInput,
    user: Annotated[db.user.User, Depends(helpers.get_user)],
):
    conversation = db.conversation.Conversation(
        title=input.title,
        owner_id=user.id,
    )
    db.conversation.create_conversation(conversation)
    return conversation


@router.delete("/conversation/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    _user: Annotated[db.user.User, Depends(helpers.get_user)],
):
    db.conversation.delete_conversation(uuid.UUID(conversation_id))
    return {"success": True}


@router.get("/conversation/{conversation_id}")
async def get_messages(
    conversation_id: str,
    _user: Annotated[db.user.User, Depends(helpers.get_user)],
):
    return db.conversation.get_messages_of_conversation(uuid.UUID(conversation_id))


@router.post("/conversation/{conversation_id}/chat")
async def chat_in_conversation(
    conversation_id: str,
    input: ChatInput,
    _user: Annotated[db.user.User, Depends(helpers.get_user)],
):
    old_messages = db.conversation.get_messages_of_conversation(
        uuid.UUID(conversation_id)
    )
    # TODO: Save the new question and its answer to the database
    output = chain.stream(
        {
            "question": input.question + " according to sources of IIT Bombay",
            "chat_history": "\n\n".join(
                [f"{msg.role}: {msg.content}" for msg in old_messages]
            )
            or "None",
        },
        # Uncomment the line below to turn on debug mode
        # config=llm.generator.debug_config,
    )

    return StreamingResponse(output, media_type="text/plain")
