from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

RESPONSES_FILE = 'responses.json'
CONTACTS_FILE = 'contacts.json'
SETTINGS_FILE = 'settings.json'

# פונקציות עזר
def load_json(file_path, default_data):
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# קריאה ראשונית של קבצים
responses = load_json(RESPONSES_FILE, [])
contacts = load_json(CONTACTS_FILE, [])
settings = load_json(SETTINGS_FILE, {"INFORU_USER": "", "INFORU_PASS": "", "SENDER": ""})

@app.route('/')
def home():
    return "SMS Bot API is Running!"

# תגובות
@app.route('/responses', methods=['GET'])
def get_responses():
    return jsonify(responses)

@app.route('/responses', methods=['POST'])
def add_response():
    data = request.get_json()
    responses.append({"incoming": data['incoming'], "reply": data['reply']})
    save_json(RESPONSES_FILE, responses)
    return jsonify({"status": "response added"})

@app.route('/responses/<int:index>', methods=['DELETE'])
def delete_response(index):
    if 0 <= index < len(responses):
        responses.pop(index)
        save_json(RESPONSES_FILE, responses)
        return jsonify({"status": "response deleted"})
    return jsonify({"status": "invalid index"}), 400

# אנשי קשר
@app.route('/contacts', methods=['GET'])
def get_contacts():
    return jsonify(contacts)

@app.route('/contacts', methods=['POST'])
def add_contact():
    data = request.get_json()
    contacts.append({"name": data['name'], "phone": data['phone']})
    save_json(CONTACTS_FILE, contacts)
    return jsonify({"status": "contact added"})

@app.route('/contacts/<int:index>', methods=['DELETE'])
def delete_contact(index):
    if 0 <= index < len(contacts):
        contacts.pop(index)
        save_json(CONTACTS_FILE, contacts)
        return jsonify({"status": "contact deleted"})
    return jsonify({"status": "invalid index"}), 400

# הגדרות חיבור ל־Inforu
@app.route('/settings', methods=['GET'])
def get_settings():
    return jsonify(settings)

@app.route('/settings', methods=['POST'])
def update_settings():
    data = request.get_json()
    settings.update({
        "INFORU_USER": data['INFORU_USER'],
        "INFORU_PASS": data['INFORU_PASS'],
        "SENDER": data['SENDER']
    })
    save_json(SETTINGS_FILE, settings)
    return jsonify({"status": "settings updated"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
