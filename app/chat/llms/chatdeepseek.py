from langchain_deepseek import ChatDeepSeek
from app.chat.models import ChatArgs

def build_llm(chat_args: ChatArgs):
    return ChatDeepSeek(
        model="deepseek-chat",
        streaming=chat_args.streaming,
    )