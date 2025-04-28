from functools import partial
from . import chatopenai
from . import chatdeepseek

llm_map = {
    'gpt-4.1-nano': partial(chatopenai.build_llm, model='gpt-4.1-nano'),
    'gpt-4.1-mini': partial(chatopenai.build_llm, model='gpt-4.1-mini'),
    'deepseek': chatdeepseek.build_llm
}