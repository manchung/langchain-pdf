from pydantic import BaseModel, Field
from typing import Any, List
from langchain.memory import ConversationBufferMemory
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

def build_memory(chat_args):
    sql_memory = SqlMessageHistory(
        conversation_id=chat_args.conversation_id
    )
    # for msg in sql_memory.messages:
    #     print(f'MANCH inside build_memory 2:{msg}')
    return ConversationBufferMemory(
        chat_memory=sql_memory,
        return_messages=True,
        memory_key="chat_history",
        output_key="answer"
    )