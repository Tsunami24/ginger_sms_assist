user_contexts = {}

def get_user_context(user_id):
    return user_contexts.get(user_id, "")

def update_user_context(user_id, message, response):
    context = user_contexts.get(user_id, "")
    context += f"\nUser: {message}\nGinger: {response}"
    user_contexts[user_id] = context[-1000:]  # Keep last 1000 characters as context