from functools import lru_cache

@lru_cache(maxsize=100)
def cached_generate_response(message, context):
    from utils.openai_handler import generate_response
    return generate_response(message, context)