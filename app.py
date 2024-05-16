from flask import Flask, request, jsonify
import requests
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()



app = Flask(__name__)

# Endpoint to receive POST requests
@app.route('/demo-webhook', methods=['POST'])
def webhook():
    payload = request.json
    if payload['type'] == 'message':
        send_whatsapp_reply(payload['payload']['sender']['phone'],payload['payload']['payload']['text'])
    return '', 200


def send_whatsapp_reply(phone_number,message):
        # Extract data from request
        # Call a hypothetical method to get API key by store ID and tenant ID
        # api_key = get_api_key_by_store_id(store_id, tenant_id)

        # Prepare request data
        url = "https://api.gupshup.io/wa/api/v1/msg"
    

        payload = {
            "source": "918037203216",
            "src.name": "Peeperly",
            "destination": phone_number,
            "message": generate_reply(message),
            "channel": "whatsapp",
            "disablePreview": False
        }

        headers = {
            "accept": "application/json",
            "apikey": os.getenv("gupshup_api_key")
        }
        response = requests.post(url, data=payload, headers=headers)
        return True



# Set your OpenAI API key

def generate_reply(message):
    openai.api_key = os.getenv("openai_api_key")


    response = openai.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt=f"You: {message}\nAI:"
    )
    reply = response.choices[0].text.strip()
    return reply



if __name__ == '__main__':
    app.run(debug=True)
