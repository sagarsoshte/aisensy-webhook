from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/call-completed', methods=['POST'])
def call_completed():
    data = request.json
    phone_number = data.get('phone')

    if not phone_number:
        return jsonify({"error": "Phone number missing"}), 400

    aisensy_url = "https://backend.aisensy.com/campaign/t1/api/v2"
    
    payload = {
        "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1NTg0Njc0NGM2ODkzMDljMjIxMjBiOSIsIm5hbWUiOiJQYXdhbiBBZ3JvIiwiYXBwTmFtZSI6IkFpU2Vuc3kiLCJjbGllbnRJZCI6IjY1MWY5MDdhOGI4MGJmMGJlMTdhOTRkYSIsImFjdGl2ZVBsYW4iOiJOT05FIiwiaWF0IjoxNzAwMjg0MDIwfQ.CAvpxNTLITpfzhUULS1-_dKKgQ_lNoRVYiJaJspdBZI",         # ✅ Required in payload
        "campaignName": "thank-you",           # ✅ Must match your AiSensy live campaign
        "destination": phone_number,                # ✅ E.g., +919876543210
        "userName": "Customer",                     # ✅ Required
        "source": "Telecalling",                    # Optional
        "templateParams": ["Customer"],             # Optional
        "tags": ["call-followup"]                   # Optional
    }

    headers = {
        "Content-Type": "application/json"
    }

    res = requests.post(aisensy_url, json=payload, headers=headers)

    try:
        return jsonify({"aisensy_response": res.json()}), res.status_code
    except Exception as e:
        return jsonify({"error": "Could not parse response", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
