from typing import Any
import uuid

from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult

from instigpt.db import conversation as db_conversation


class SaveResponseToDBCallback(BaseCallbackHandler):
    def __init__(self, conversation_id: uuid.UUID) -> None:
        self.conversation_id = conversation_id
        super().__init__()

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        message = db_conversation.Message(
            role=db_conversation.MessageRole.ASSISTANT,
            conversation_id=self.conversation_id,
            content=response.generations[0][0].text,
        )
        db_conversation.create_message(message)
