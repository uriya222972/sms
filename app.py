from flask import Flask, request, jsonify, send_from_directory
import os
import json

app = Flask(__name__)

# נתיבי קבצים
USERS_FILE = 'users.json'

# עוזרים
def load_json(file_path, default_data):
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# קריאה ראשונית של משתמשים
users = load_json(USERS_FILE, {})

# דף הבית: משרת את index.html
@app.route('/')
def serve_index():
    return send_from_directory('', 'index.html')

# התחברות
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username in users and users[username]['password'] == password:
        return jsonify({
            "status": "success",
            "role": users[username]['role'],
            "tabs": users[username]['tabs'],
            "sender": users[username]['sender']
        })
    else:
        return jsonify({"status": "fail"}), 401

# תגובות (לפי משתמש)
@app.route('/responses', methods=['GET', 'POST', 'DELETE'])
def handle_responses():
    username = request.args.get('user')
    if not username:
        return jsonify({"status": "fail", "message": "User required"}), 400
    file = f'responses_{username}.json'
    responses = load_json(file, [])
    if request.method == 'GET':
        return jsonify(responses)
    elif request.method == 'POST':
        data = request.get_json()
        responses.append({"incoming": data['incoming'], "reply": data['reply']})
        save_json(file, responses)
        return jsonify({"status": "response added"})
    elif request.method == 'DELETE':
        index = int(request.args.get('index'))
        if 0 <= index < len(responses):
            responses.pop(index)
            save_json(file, responses)
            return jsonify({"status": "response deleted"})
        return jsonify({"status": "invalid index"}), 400

# אנשי קשר (לפי משתמש)
@app.route('/contacts', methods=['GET', 'POST', 'DELETE'])
def handle_contacts():
    username = request.args.get('user')
    if not username:
        return jsonify({"status": "fail", "message": "User required"}), 400
    file = f'contacts_{username}.json'
    contacts = load_json(file, [])
    if request.method == 'GET':
        return jsonify(contacts)
    elif request.method == 'POST':
        data = request.get_json()
        contacts.append({"name": data['name'], "phone": data['phone']})
        save_json(file, contacts)
        return jsonify({"status": "contact added"})
    elif request.method == 'DELETE':
        index = int(request.args.get('index'))
        if 0 <= index < len(contacts):
            contacts.pop(index)
            save_json(file, contacts)
            return jsonify({"status": "contact deleted"})
        return jsonify({"status": "invalid index"}), 400

# ניהול משתמשים (admin בלבד בהמשך נרחיב)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
