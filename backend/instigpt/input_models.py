from pydantic import BaseModel


class ChatInput(BaseModel):
    question: str
    chat_history: list[str] | None
