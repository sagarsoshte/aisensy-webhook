from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/call-completed', methods=['POST'])
def call_completed():
    # Try to get the phone number from JSON, form, or query string
    phone = (
        (request.json or {}).get("phone") or
        request.form.get("phone") or
        request.args.get("phone")
    )

    if not phone:
        return jsonify({"error": "Phone number missing"}), 400

    # Add +91 prefix if not already present
    if not phone.startswith("+"):
        phone = "+91" + phone

    # AiSensy API payload
    payload = {
        "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1NTg0Njc0NGM2ODkzMDljMjIxMjBiOSIsIm5hbWUiOiJQYXdhbiBBZ3JvIiwiYXBwTmFtZSI6IkFpU2Vuc3kiLCJjbGllbnRJZCI6IjY1MWY5MDdhOGI4MGJmMGJlMTdhOTRkYSIsImFjdGl2ZVBsYW4iOiJOT05FIiwiaWF0IjoxNzAwMjg0MDIwfQ.CAvpxNTLITpfzhUULS1-_dKKgQ_lNoRVYiJaJspdBZI",  # 🔐 Replace with your actual API key
        "campaignName": "thank-you",    # 🧾 Must match your AiSensy campaign name exactly
        "destination": phone,
        "userName": "Customer",
        "source": "Telecalling",
        "templateParams": [],  # 🔁 Match the variables in your template
        "tags": ["call-followup"]
    }

    headers = {"Content-Type": "application/json"}

    # Send POST request to AiSensy
    response = requests.post("https://backend.aisensy.com/campaign/t1/api/v2", json=payload, headers=headers)

    try:
        return jsonify({"aisensy_response": response.json()}), response.status_code
    except Exception as e:
        return jsonify({"error": "Failed to parse AiSensy response", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
