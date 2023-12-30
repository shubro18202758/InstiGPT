from typing import Sequence, List
import enum
from datetime import datetime
import uuid

from sqlmodel import SQLModel, Field, Relationship, Session, select
from sqlalchemy import Uuid, Enum

from . import get_engine


class Conversation(SQLModel, table=True):
    id: uuid.UUID = Field(
        sa_type=Uuid(as_uuid=True),
        default_factory=uuid.uuid4,
        primary_key=True,
        description="The id of the conversation",
    )
    title: str = Field(description="The title of the conversation")
    owner_id: int = Field(
        description="The ID of the user that the conversation belongs to",
        foreign_key="user.id",
    )
    created_at: datetime = Field(
        description="The time when the conversation was created",
        default_factory=datetime.now,
    )

    messages: List["Message"] = Relationship(back_populates="conversation")


class MessageRole(enum.Enum):
    ASSISTANT = "assistant"
    USER = "user"


class Message(SQLModel, table=True):
    id: uuid.UUID = Field(
        sa_type=Uuid(as_uuid=True),
        default_factory=uuid.uuid4,
        primary_key=True,
        description="The id of the message",
    )
    content: str = Field(description="The title of the conversation")
    role: MessageRole = Field(
        sa_type=Enum(MessageRole),
        description="The role of the user that sent the message",
    )
    created_at: datetime = Field(
        description="The time when the message was created",
        default_factory=datetime.now,
    )

    conversation_id: int = Field(
        description="The ID of the conversation that the message belongs to",
        foreign_key="conversation.id",
    )
    conversation: Conversation = Relationship(back_populates="messages")


def get_conversations_of_user(user_id: int) -> Sequence[Conversation]:
    with Session(get_engine()) as session:
        statement = select(Conversation).where(Conversation.owner_id == user_id)
        conversations = session.exec(statement).all()

    return conversations


def get_messages_of_conversation(conversation_id: uuid.UUID) -> Sequence[Message]:
    with Session(get_engine()) as session:
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)  # type: ignore
        )
        messages = session.exec(statement).all()

    return messages


def create_conversation(conversation: Conversation):
    with Session(get_engine(), expire_on_commit=False) as session:
        session.add(conversation)
        session.commit()


def delete_conversation(conversation_id: uuid.UUID):
    with Session(get_engine()) as session:
        statement = select(Conversation).where(Conversation.id == conversation_id)
        conversation = session.exec(statement).first()
        if conversation is None:
            return

        statement = select(Message).where(Message.conversaton_id == conversation_id)
        messages = session.exec(statement).all()

        session.delete(messages)
        session.delete(conversation)
        session.commit()


def create_message(message: Message):
    with Session(get_engine(), expire_on_commit=False) as session:
        session.add(message)
        session.commit()
