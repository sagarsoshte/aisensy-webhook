from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/call-completed', methods=['POST'])
def call_completed():
    # 🔍 DEBUG: Print everything received in the request
    print("🔔 Webhook hit!")
    print("Headers:", dict(request.headers))
    print("Form data:", request.form.to_dict())
    print("Query args:", request.args.to_dict())
    print("JSON body:", request.get_json(silent=True))

    # Get phone number from any possible source
    phone = (
        (request.json or {}).get("phone") if request.is_json else None
    ) or request.form.get("phone") or request.args.get("phone")

    if not phone:
        return jsonify({
            "error": "Phone number missing",
            "received": {
                "form": request.form.to_dict(),
                "args": request.args.to_dict(),
                "json": request.get_json(silent=True)
            }
        }), 400

    # Format phone with country code if needed
    if not phone.startswith("+"):
        phone = "+91" + phone

    # Build payload for AiSensy
    payload = {
        "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1NTg0Njc0NGM2ODkzMDljMjIxMjBiOSIsIm5hbWUiOiJQYXdhbiBBZ3JvIiwiYXBwTmFtZSI6IkFpU2Vuc3kiLCJjbGllbnRJZCI6IjY1MWY5MDdhOGI4MGJmMGJlMTdhOTRkYSIsImFjdGl2ZVBsYW4iOiJOT05FIiwiaWF0IjoxNzAwMjg0MDIwfQ.CAvpxNTLITpfzhUULS1-_dKKgQ_lNoRVYiJaJspdBZI",  # 🔐 Replace with your AiSensy API Key
        "campaignName": "thank-you",    # Must match exact AiSensy campaign
        "destination": phone,
        "userName": "Customer",
        "source": "Telecalling",
        "templateParams": [],  # Match number of {{}} in your template
        "tags": ["call-followup"]
    }

    headers = {"Content-Type": "application/json"}

    # Send to AiSensy
    try:
        response = requests.post("https://backend.aisensy.com/campaign/t1/api/v2", json=payload, headers=headers)
        return jsonify({
            "aisensy_response": response.json(),
            "received": {
                "form": request.form.to_dict(),
                "args": request.args.to_dict(),
                "json": request.get_json(silent=True)
            }
        }), response.status_code
    except Exception as e:
        return jsonify({
            "error": "Error sending to AiSensy",
            "details": str(e)
        }), 500

# Optional: Run locally if needed
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
