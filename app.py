from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# In-memory store to track last sent time per phone
last_sent_time = {}

@app.route('/call-completed', methods=['POST'])
def call_completed():
    print("🔔 Webhook hit!")
    print("Headers:", dict(request.headers))
    print("Form data:", request.form.to_dict())
    print("Query args:", request.args.to_dict())
    print("JSON body:", request.get_json(silent=True))

    # Accept all sources (form, query, json)
    data = {}
    if request.is_json:
        data = request.get_json()
    data.update(request.form.to_dict())
    data.update(request.args.to_dict())

    phone = data.get("phone")
    event = data.get("Event") or data.get("event") or data.get("callType")  # try all possible variations

    if not phone:
        return jsonify({
            "error": "Phone number missing",
            "received": data
        }), 400

    if not event:
        return jsonify({
            "error": "Call event type missing (e.g., Incoming/Outgoing)",
            "received": data
        }), 400

    # ✅ Only allow Incoming calls
    if event.strip().lower() != "incoming":
        return jsonify({
            "message": f"Ignored: Not an incoming call (Event='{event}')"
        }), 200

    if not phone.startswith("+"):
        phone = "+91" + phone

    now = datetime.utcnow()
    last_time = last_sent_time.get(phone)
    if last_time and now - last_time < timedelta(hours=24):
        return jsonify({
            "message": f"Message already sent to {phone} within 24 hours",
            "last_sent": last_time.isoformat()
        }), 200

    payload = {
        "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1NTg0Njc0NGM2ODkzMDljMjIxMjBiOSIsIm5hbWUiOiJQYXdhbiBBZ3JvIiwiYXBwTmFtZSI6IkFpU2Vuc3kiLCJjbGllbnRJZCI6IjY1MWY5MDdhOGI4MGJmMGJlMTdhOTRkYSIsImFjdGl2ZVBsYW4iOiJOT05FIiwiaWF0IjoxNzAwMjg0MDIwfQ.CAvpxNTLITpfzhUULS1-_dKKgQ_lNoRVYiJaJspdBZI",  # Replace this with actual API key
        "campaignName": "thank-you",
        "destination": phone,
        "userName": "Customer",
        "source": "Telecalling",
        "templateParams": [],
        "tags": ["call-followup"]
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post("https://backend.aisensy.com/campaign/t1/api/v2", json=payload, headers=headers)
        if response.status_code == 200:
            last_sent_time[phone] = now

        return jsonify({
            "aisensy_response": response.json(),
            "sent_at": now.isoformat()
        }), response.status_code

    except Exception as e:
        return jsonify({
            "error": "Error sending to AiSensy",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
