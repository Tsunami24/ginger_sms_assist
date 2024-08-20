import openai
from config import Config

openai.api_key = Config.OPENAI_API_KEY

def generate_response(message, context):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Ginger, a helpful AI assistant."},
            {"role": "user", "content": f"Context: {context}\n\nUser: {message}"}
        ]
    )
    return response.choices[0].message['content'].strip()