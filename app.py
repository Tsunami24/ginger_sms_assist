from flask import Flask, request, jsonify
from utils.vonage_handler import receive_sms, send_sms
from utils.openai_handler import generate_response
from utils.user_handler import get_user_context, update_user_context
from config import Config
import logging

app = Flask(__name__)
app.config.from_object(Config)

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route('/webhook', methods=['POST'])
def webhook():
    app.logger.info("Received webhook")
    data = request.get_json()
    app.logger.info(f"Webhook data: {data}")

    if not data:
        app.logger.error("No data received in webhook")
        return jsonify({"status": "error", "message": "No data received"}), 400

    sender = data.get('from')
    message = data.get('text')

    if not sender or not message:
        app.logger.error(f"Missing sender or message. Sender: {sender}, Message: {message}")
        return jsonify({"status": "error", "message": "Missing sender or message"}), 400

    app.logger.info(f"Processing message from {sender}: {message}")

    # Get user context
    user_context = get_user_context(sender)

    # Generate AI response
    ai_response = generate_response(message, user_context)

    # Update user context
    update_user_context(sender, message, ai_response)

    # Send response via SMS
    send_sms(sender, ai_response)

    app.logger.info(f"Sent response to {sender}: {ai_response}")

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True)