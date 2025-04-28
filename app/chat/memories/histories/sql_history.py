from pydantic import BaseModel, Field
from typing import Any, List
from langchain.schema import BaseChatMessageHistory

from app.web.api import (
    get_messages_by_conversation_id,
    add_message_to_conversation
)
class SqlMessageHistory(BaseChatMessageHistory):
    conversation_id: str
    messages: list[Any] = Field(default_factory=lambda: [])
    
    def __init__(self, conversation_id):
        super().__init__()
        self.conversation_id = conversation_id
        self.messages = get_messages_by_conversation_id(self.conversation_id)
    
    # @property
    # def messages(self) -> List[Any]:
    #     return ['garbage']
    #     # return get_messages_by_conversation_id(self.conversation_id)
    
    def add_message(self, message):
        res = add_message_to_conversation(
            conversation_id=self.conversation_id,
            role=message.type,
            content=message.content
        )
        self.messages = get_messages_by_conversation_id(self.conversation_id)
        return res

    def clear(self):
        pass
