from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# responses
responses = [
    {"incoming": "שלום", "reply": "שלום וברכה!"},
    {"incoming": "מה נשמע", "reply": "הכל מצוין, תודה!"}
]

# פרטי Inforu מהסביבה
INFORU_USER = os.environ.get('INFORU_USER')
INFORU_PASS = os.environ.get('INFORU_PASS')
SENDER = os.environ.get('SENDER')

def send_sms(phone, message):
    url = "https://uapi.inforu.co.il/SendMessageXml.ashx"
    xml = f"""
    <Inforu>
      <User>
        <Username>{INFORU_USER}</Username>
        <Password>{INFORU_PASS}</Password>
      </User>
      <Content Type="sms">
        <Message>{message}</Message>
      </Content>
      <Recipients>
        <PhoneNumber>{phone}</PhoneNumber>
      </Recipients>
      <Settings>
        <Sender>{SENDER}</Sender>
      </Settings>
    </Inforu>
    """
    headers = {"Content-Type": "text/xml"}
    response = requests.post(url, data=xml.encode('utf-8'), headers=headers)
    return response.text

@app.route('/')
def home():
    return "SMS Bot is Running!"

@app.route('/inbound_sms', methods=['POST'])
def inbound_sms():
    data = request.form
    incoming_text = data.get('Message')
    phone_number = data.get('Phone')

    if incoming_text and phone_number:
        matched = next((r['reply'] for r in responses if r['incoming'] == incoming_text), None)
        if matched:
            send_sms(phone_number, matched)
            return jsonify({"status": "replied", "reply": matched})
        else:
            return jsonify({"status": "no match"})
    else:
        return jsonify({"status": "invalid request"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
