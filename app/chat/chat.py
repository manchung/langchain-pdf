import random, os
from langchain.chains import ConversationalRetrievalChain
from app.chat.models import ChatArgs
from app.chat.vector_stores import retriever_map
from app.chat.llms import llm_map
from app.chat.memories import memory_map
from app.web.api import set_conversation_components, get_conversation_components
from app.chat.score import random_component_by_score
# from app.chat.tracing.langfuse import langfuse
from langfuse.callback import CallbackHandler
from langfuse import Langfuse
from langchain.callbacks.manager import CallbackManager

def select_component(component_type, component_map, chat_args):
    components = get_conversation_components(chat_args.conversation_id)
    
    component = None
    previous_component = components[component_type]
    if previous_component:
        builder = component_map[previous_component]
        return previous_component, builder(chat_args)
    else:
        random_component_name = random_component_by_score(component_type, component_map)
        builder = component_map[random_component_name]
        return random_component_name, builder(chat_args)



def build_chat(chat_args: ChatArgs):
    """
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.

    :return: A chain

    Example Usage:

        chain = build_chat(chat_args)
    """
    retriever_name, retriever = select_component('retriever', retriever_map, chat_args)
    llm_name, llm = select_component('llm', llm_map, chat_args)
    memory_name, memory = select_component('memory', memory_map, chat_args)
    
    # print(f'Running with llm: {llm_name}  retriever: {retriever_name}  memory: {memory_name}')
    set_conversation_components(
        conversation_id=chat_args.conversation_id,
        retriever=retriever_name,
        llm=llm_name,
        memory=memory_name
    )

    langfuse = Langfuse(             # kwargs override env-vars if you want
        public_key = os.environ['LANGFUSE_PUBLIC_KEY'],
        secret_key = os.environ['LANGFUSE_SECRET_KEY'],
        host       = os.environ['LANGFUSE_HOST'],
    )
    trace = langfuse.trace(
        id = chat_args.conversation_id,
        metadata=chat_args.metadata.to_dict(),
    )
    
    langfuse_handler = trace.get_langchain_handler()
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=memory,
        retriever=retriever,
        # metadata=chat_args.metadata.to_dict(),
        callbacks=[langfuse_handler],
    )
    
