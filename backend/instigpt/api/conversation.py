from typing import Annotated
import uuid

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from instigpt import llm
from instigpt.db import (
    conversation as db_conversation,
    user as db_user,
)

from . import helpers
from .input_models import ChatInput, CreateConversationInput

router = APIRouter()

embeddings = llm.get_embeddings()
model = llm.get_generator_model()
retriever = llm.get_retriever(embeddings=embeddings)
chain = llm.get_chain(llm=model, retriever=retriever)


@router.get("/conversation")
async def get_conversations(user: Annotated[db_user.User, Depends(helpers.get_user)]):
    return db_conversation.get_conversations_of_user(user.id)


@router.post("/conversation")
async def create_conversation(
    input: CreateConversationInput,
    user: Annotated[db_user.User, Depends(helpers.get_user)],
):
    conversation = db_conversation.Conversation(
        title=input.title,
        owner_id=user.id,
    )
    db_conversation.create_conversation(conversation)
    return conversation


@router.delete("/conversation/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    _user: Annotated[db_user.User, Depends(helpers.get_user)],
):
    db_conversation.delete_conversation(uuid.UUID(conversation_id))
    return {"success": True}


@router.get("/conversation/{conversation_id}")
async def get_messages(
    conversation_id: str,
    _user: Annotated[db_user.User, Depends(helpers.get_user)],
):
    return db_conversation.get_messages_of_conversation(uuid.UUID(conversation_id))


@router.post("/conversation/{conversation_id}/chat")
async def chat_in_conversation(
    conversation_id: str,
    input: ChatInput,
    _user: Annotated[db_user.User, Depends(helpers.get_user)],
):
    conv_id = uuid.UUID(conversation_id)

    # Get the old messages
    old_messages = db_conversation.get_messages_of_conversation(conv_id)

    # Store the new question in the database
    message = db_conversation.Message(
        role=db_conversation.MessageRole.USER,
        conversation_id=conv_id,
        content=input.question,
    )
    db_conversation.create_message(message)

    # Generate the response
    output = chain.stream(
        {
            "question": input.question + " according to sources of IIT Bombay",
            "chat_history": "\n\n".join(
                [f"{msg.role}: {msg.content}" for msg in old_messages]
            )
            or "None",
        },
        # NOTE: This config registers a callback handler that saves the response to the database
        config=llm.generator.get_config(conv_id),
    )

    return StreamingResponse(output, media_type="text/plain")
