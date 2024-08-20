import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    VONAGE_API_KEY = os.environ.get('VONAGE_API_KEY')
    VONAGE_API_SECRET = os.environ.get('VONAGE_API_SECRET')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    VONAGE_FROM_NUMBER = os.environ.get('VONAGE_FROM_NUMBER')

    @classmethod
    def check_config(cls):
        print("Checking configuration...")
        for attr in ['VONAGE_API_KEY', 'VONAGE_API_SECRET', 'OPENAI_API_KEY', 'VONAGE_FROM_NUMBER']:
            value = getattr(cls, attr)
            print(f"{attr}: {'*' * len(value) if value else 'Not set'}")
        
        missing = [attr for attr in ['VONAGE_API_KEY', 'VONAGE_API_SECRET', 'OPENAI_API_KEY', 'VONAGE_FROM_NUMBER'] if not getattr(cls, attr)]
        if missing:
            raise ValueError(f"Missing configuration: {', '.join(missing)}")
        print("Configuration check complete.")