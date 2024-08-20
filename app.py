from flask import Flask, request, jsonify
from utils.vonage_handler import receive_sms, send_sms
from utils.openai_handler import generate_response
from utils.user_handler import get_user_context, update_user_context
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    # Process incoming SMS
    sender = data['from']
    message = data['text']
    
    # Get user context
    user_context = get_user_context(sender)
    
    # Generate AI response
    ai_response = generate_response(message, user_context)
    
    # Update user context
    update_user_context(sender, message, ai_response)
    
    # Send response via SMS
    send_sms(sender, ai_response)
    
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True)