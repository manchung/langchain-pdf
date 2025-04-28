from langchain.memory import ConversationBufferWindowMemory
from app.chat.memories.histories.sql_history import SqlMessageHistory

def window_buffer_memory_builder(chat_args):
    sql_memory = SqlMessageHistory(
        conversation_id=chat_args.conversation_id
    )
    # for msg in sql_memory.messages:
    #     print(f'MANCH inside build_memory 2:{msg}')
    return ConversationBufferWindowMemory(
        chat_memory=sql_memory,
        return_messages=True,
        memory_key="chat_history",
        output_key="answer",
        k=2
    )