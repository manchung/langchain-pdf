from langchain_openai import ChatOpenAI
from app.chat.models import ChatArgs

def build_llm(chat_args: ChatArgs, model: str):
    return ChatOpenAI(
        model=model,
        streaming=chat_args.streaming,
    )