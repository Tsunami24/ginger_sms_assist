import vonage
from config import Config
import logging

client = vonage.Client(key=Config.VONAGE_API_KEY, secret=Config.VONAGE_API_SECRET)
sms = vonage.Sms(client)

def send_sms(to, text):
    if not Config.VONAGE_FROM_NUMBER:
        logging.error("VONAGE_FROM_NUMBER is not set in the configuration")
        return

    response = sms.send_message({
        'from': Config.VONAGE_FROM_NUMBER,
        'to': to,
        'text': text,
    })
    
    if response['messages'][0]['status'] == '0':
        logging.info(f"Message sent successfully to {to}")
    else:
        logging.error(f"Message failed with error: {response['messages'][0]['error-text']}")