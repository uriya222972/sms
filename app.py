
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# פרטי החיבור ל־InforU
INFORU_USERNAME = "22uriya22"
INFORU_TOKEN = "4a549e05-8668-448f-b3a7-5ee7816ee0ad"
INFORU_SENDER = "0537038545"

@app.route('/send_sms', methods=['POST'])
def send_sms():
    data = request.json
    phone = data.get("phone")
    message = data.get("message")

    payload = {
        "Auth": {
            "Username": INFORU_USERNAME,
            "Token": INFORU_TOKEN
        },
        "Content": {
            "Message": message
        },
        "Recipients": {
            "RecipientsPhone": [phone]
        },
        "Settings": {
            "Sender": INFORU_SENDER
        }
    }

    try:
        res = requests.post("https://capi.inforu.co.il/api/v2/SendSms", json=payload)
        return jsonify(res.json()), res.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
