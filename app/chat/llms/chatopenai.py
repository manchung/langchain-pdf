from langchain_openai import ChatOpenAI
from app.chat.models import ChatArgs

def build_llm(chat_args: ChatArgs):
    return ChatOpenAI(
        # model="gpt-4.1-nano",
    )