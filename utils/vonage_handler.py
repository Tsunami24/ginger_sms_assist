import vonage
from config import Config

client = vonage.Client(key=Config.VONAGE_API_KEY, secret=Config.VONAGE_API_SECRET)
sms = vonage.Sms(client)

def receive_sms(data):
    # This function is not needed as we're handling incoming SMS in the webhook
    pass

def send_sms(to, text):
    response = sms.send_message({
        'from': Config.VONAGE_FROM_NUMBER,
        'to': to,
        'text': text,
    })
    if response['messages'][0]['status'] == '0':
        print(f"Message sent successfully to {to}")
    else:
        print(f"Message failed with error: {response['messages'][0]['error-text']}")