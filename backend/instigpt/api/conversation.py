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
search_results_retriever = llm.get_search_results_retriever()
chain = llm.get_chain(
    llm=model,
    retriever=retriever,
    search_results_retriever=search_results_retriever,
)


@router.get("/conversation")
async def get_conversations(user: Annotated[db_user.User, Depends(helpers.get_user)]):
    return {"conversations": db_conversation.get_conversations_of_user(user.id)}


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
    return {"conversation": conversation}


@router.delete("/conversation/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    _user: Annotated[db_user.User, Depends(helpers.get_user)],
):
    db_conversation.delete_conversation(uuid.UUID(conversation_id))
    return {"success": True}


@router.patch("/conversation/{conversation_id}")
async def updaet_conversation(
    conversation_id: str,
    input: CreateConversationInput,
    _user: Annotated[db_user.User, Depends(helpers.get_user)],
):
    updated_conversation = db_conversation.update_conversation(
        uuid.UUID(conversation_id), input.title
    )
    return {"conversation": updated_conversation}


@router.get("/conversation/{conversation_id}")
async def get_messages(
    conversation_id: str,
    _user: Annotated[db_user.User, Depends(helpers.get_user)],
):
    return {
        "messages": db_conversation.get_messages_of_conversation(
            uuid.UUID(conversation_id)
        )
    }


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
    question_message = db_conversation.Message(
        role=db_conversation.MessageRole.USER,
        conversation_id=conv_id,
        content=input.question,
    )
    db_conversation.create_message(question_message)

    # Generate the response
    output = chain.invoke(
        {
            "question": input.question,
            "chat_history": "\n\n".join(
                [
                    f"{msg.role.value.upper()}: {msg.content}"
                    for msg in old_messages[:-1]
                ]
            )
            or "None",
        },
        # Uncomment this to use the debug config
        # config=llm.generator.debug_config,
    )
    # Store the response in the database
    response_message = db_conversation.Message(
        role=db_conversation.MessageRole.ASSISTANT,
        conversation_id=conv_id,
        content=output,
    )
    db_conversation.create_message(response_message)

    return {"new_messages": [question_message, response_message]}
