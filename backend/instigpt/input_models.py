from pydantic import BaseModel


class Chat(BaseModel):
    role: str
    content: str

    def __str__(self):
        return f"{self.role}: {self.content}"


class ChatInput(BaseModel):
    messages: list[Chat]
