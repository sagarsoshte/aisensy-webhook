from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/call-completed', methods=['POST'])
def call_completed():
    # Accept phone from JSON, form, or query string
    phone = (
        (request.json or {}).get("phone") or
        request.form.get("phone") or
        request.args.get("phone")
    )

    if not phone:
        return jsonify({"error": "Phone number missing"}), 400

    # Ensure phone number includes +91
    if not phone.startswith("+"):
        phone = "+91" + phone

    payload = {
        "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1NTg0Njc0NGM2ODkzMDljMjIxMjBiOSIsIm5hbWUiOiJQYXdhbiBBZ3JvIiwiYXBwTmFtZSI6IkFpU2Vuc3kiLCJjbGllbnRJZCI6IjY1MWY5MDdhOGI4MGJmMGJlMTdhOTRkYSIsImFjdGl2ZVBsYW4iOiJOT05FIiwiaWF0IjoxNzAwMjg0MDIwfQ.CAvpxNTLITpfzhUULS1-_dKKgQ_lNoRVYiJaJspdBZI",
        "campaignName": "thank-you",  # Must match AiSensy
        "destination": phone,
        "userName": "Customer",
        "source": "Telecalling",
        "templateParams": ["Customer"],  # Match your template
        "tags": ["call-followup"]
    }

    res = requests.post("https://backend.aisensy.com/campaign/t1/api/v2", json=payload)

    try:
        return jsonify({"aisensy_response": res.json()}), res.status_code
    except Exception as e:
        return jsonify({"error": "Failed to parse AiSensy response", "details": str(e)}), 500
