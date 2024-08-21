import os
from dotenv import load_dotenv

print("Current working directory:", os.getcwd())
print("Contents of .env file:")
with open('.env', 'r') as f:
    print(f.read())

load_dotenv()

class Config:
    VONAGE_API_KEY = os.environ.get('VONAGE_API_KEY')
    VONAGE_API_SECRET = os.environ.get('VONAGE_API_SECRET')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    VONAGE_FROM_NUMBER = os.environ.get('VONAGE_FROM_NUMBER')

    @classmethod
    def check_config(cls):
        print("Checking configuration...")
        print("Environment variables:")
        for key, value in os.environ.items():
            if key in ['VONAGE_API_KEY', 'VONAGE_API_SECRET', 'OPENAI_API_KEY', 'VONAGE_FROM_NUMBER']:
                print(f"{key}: {'*' * len(value) if value else 'Not set'}")
        
        for attr in ['VONAGE_API_KEY', 'VONAGE_API_SECRET', 'OPENAI_API_KEY', 'VONAGE_FROM_NUMBER']:
            value = getattr(cls, attr)
            print(f"{attr}: {'*' * len(value) if value else 'Not set'}")
        
        missing = [attr for attr in ['VONAGE_API_KEY', 'VONAGE_API_SECRET', 'OPENAI_API_KEY', 'VONAGE_FROM_NUMBER'] if not getattr(cls, attr)]
        if missing:
            print("\nMissing configuration detected!")
            print("Please ensure all required environment variables are set.")
            print("You can set them in your .env file for local development,")
            print("or use 'heroku config:set' for your Heroku deployment.")
            print(f"\nMissing variables: {', '.join(missing)}")
            raise ValueError(f"Missing configuration: {', '.join(missing)}")
        print("Configuration check complete.")