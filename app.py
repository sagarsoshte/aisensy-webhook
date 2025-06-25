from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/call-completed', methods=['POST'])
def call_completed():
    data = request.json
    phone_number = data.get('phone')

    if not phone_number:
        return jsonify({"error": "Phone number missing"}), 400

    aisensy_url = "https://backend.aisensy.com/campaign/t1/api/v2/send"
    payload = {
        "campaign_name": "example",  # Update this to your AiSensy campaign
        "destination": phone_number,
        "user_ref_id": f"call_{phone_number}"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1NTg0Njc0NGM2ODkzMDljMjIxMjBiOSIsIm5hbWUiOiJQYXdhbiBBZ3JvIiwiYXBwTmFtZSI6IkFpU2Vuc3kiLCJjbGllbnRJZCI6IjY1MWY5MDdhOGI4MGJmMGJlMTdhOTRkYSIsImFjdGl2ZVBsYW4iOiJOT05FIiwiaWF0IjoxNzAwMjg0MDIwfQ.CAvpxNTLITpfzhUULS1-_dKKgQ_lNoRVYiJaJspdBZI"  # <-- Replace with your API key
    }

    res = requests.post(aisensy_url, json=payload, headers=headers)
    return jsonify({"aisensy_response": res.json()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
