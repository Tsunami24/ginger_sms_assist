import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    VONAGE_API_KEY = os.getenv('VONAGE_API_KEY')
    VONAGE_API_SECRET = os.getenv('VONAGE_API_SECRET')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')