import os
# from langfuse import Langfuse
from langfuse.callback import CallbackHandler   # v2.x import path

# langfuse = Langfuse(
#     os.environ['LANGFUSE_PUBLIC_KEY'],
#     os.environ['LANGFUSE_SECRET_KEY'],
#     host = os.environ['LANGFUSE_HOST'],
# )

langfuse = CallbackHandler(             # kwargs override env-vars if you want
    public_key = os.environ['LANGFUSE_PUBLIC_KEY'],
    secret_key = os.environ['LANGFUSE_SECRET_KEY'],
    host       = os.environ['LANGFUSE_HOST'],
)
