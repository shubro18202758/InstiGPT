from pydantic import BaseModel


class ChatInput(BaseModel):
    question: str


class CreateConversationInput(BaseModel):
    title: str
