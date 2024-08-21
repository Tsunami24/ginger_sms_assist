from flask import Flask, request, jsonify
from utils.vonage_handler import send_sms
from utils.openai_handler import generate_response
from utils.user_handler import get_user_context, update_user_context
from utils.cache import cached_generate_response
from config import Config
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

logging.basicConfig(level=logging.INFO)

print("Starting application...")
print("VONAGE_FROM_NUMBER:", os.environ.get('VONAGE_FROM_NUMBER'))
Config.check_config()
print("Configuration loaded.")

executor = ThreadPoolExecutor(max_workers=3)

def process_message(sender, message):
    user_context = get_user_context(sender)
    ai_response = cached_generate_response(message, user_context)
    update_user_context(sender, message, ai_response)
    send_sms(sender, ai_response)
    return ai_response

@app.route('/webhook', methods=['POST'])
def webhook():
    app.logger.info("Received webhook")
    app.logger.info(f"Request headers: {request.headers}")
    app.logger.info(f"Request form data: {request.form}")
    app.logger.info(f"Request JSON data: {request.json}")
    
    data = request.form or request.json or {}
    
    app.logger.info(f"Processed data: {data}")

    sender = data.get('msisdn') or data.get('from')
    message = data.get('text')

    if not sender or not message:
        app.logger.error(f"Missing sender or message. Sender: {sender}, Message: {message}")
        return jsonify({"status": "error", "message": "Missing sender or message"}), 400

    app.logger.info(f"Processing message from {sender}: {message}")

    try:
        future = executor.submit(process_message, sender, message)
        ai_response = future.result(timeout=25)  # 25 seconds timeout
        app.logger.info(f"Sent response to {sender}: {ai_response}")
        return jsonify({"status": "success"}), 200
    except Exception as e:
        app.logger.error(f"Error processing message: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "VONAGE_FROM_NUMBER": os.environ.get('VONAGE_FROM_NUMBER')}), 200

if __name__ == '__main__':
    app.run(debug=True)