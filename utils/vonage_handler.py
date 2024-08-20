import vonage
from config import Config
import logging
import re

client = vonage.Client(key=Config.VONAGE_API_KEY, secret=Config.VONAGE_API_SECRET)
sms = vonage.Sms(client)

def format_phone_number(number):
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', number)
    # Ensure the number starts with the country code
    if not digits_only.startswith('1'):  # Assuming US numbers
        digits_only = '1' + digits_only
    return digits_only

def send_sms(to, text):
    if not Config.VONAGE_FROM_NUMBER:
        logging.error("VONAGE_FROM_NUMBER is not set in the configuration")
        return

    from_number = format_phone_number(Config.VONAGE_FROM_NUMBER)
    to_number = format_phone_number(to)

    response = sms.send_message({
        'from': from_number,
        'to': to_number,
        'text': text,
    })
    
    if response['messages'][0]['status'] == '0':
        logging.info(f"Message sent successfully to {to_number}")
    else:
        logging.error(f"Message failed with error: {response['messages'][0]['error-text']}")