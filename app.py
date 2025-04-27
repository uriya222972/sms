from flask import Flask, request, jsonify, send_from_directory
import json
import os
import openpyxl
import requests

app = Flask(__name__)

# תיקיות שמירת קבצים
DATA_FOLDER = 'data'
RESPONSES_FOLDER = os.path.join(DATA_FOLDER, 'responses')
CONTACTS_FOLDER = os.path.join(DATA_FOLDER, 'contacts')
GROUPS_FOLDER = os.path.join(DATA_FOLDER, 'groups')
MANAGERS_FILE = os.path.join(DATA_FOLDER, 'managers.json')
USERS_FILE = os.path.join(DATA_FOLDER, 'users.json')

# קישור ל-API של Inforu
INFORU_URL = "https://uapi.inforu.co.il/SendMessageXml.ashx"

# ודא שתיקיות קיימות
for folder in [DATA_FOLDER, RESPONSES_FOLDER, CONTACTS_FOLDER, GROUPS_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# טעינת משתמשים
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# שמירת משתמשים
def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

# טעינת מנהלים
def load_managers():
    if os.path.exists(MANAGERS_FILE):
        with open(MANAGERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# שמירת מנהלים
def save_managers(managers):
    with open(MANAGERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(managers, f, ensure_ascii=False, indent=2)
# התחברות משתמש
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    users = load_users()
    username = data.get('username')
    password = data.get('password')
    user = users.get(username)
    if user and user.get('password') == password:
        return jsonify({"tabs": user.get('tabs', [])})
    return "Unauthorized", 401

# תגובות - טעינה
@app.route('/responses', methods=['GET'])
def get_responses():
    user = request.args.get('user')
    filepath = os.path.join(RESPONSES_FOLDER, f"{user}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify([])

# תגובות - שמירה
@app.route('/responses', methods=['POST'])
def save_response():
    user = request.args.get('user')
    filepath = os.path.join(RESPONSES_FOLDER, f"{user}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            responses = json.load(f)
    else:
        responses = []
    new_response = request.json
    responses.append(new_response)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(responses, f, ensure_ascii=False, indent=2)
    return 'OK'

# תגובות - מחיקה
@app.route('/responses', methods=['DELETE'])
def delete_response():
    user = request.args.get('user')
    index = int(request.args.get('index'))
    filepath = os.path.join(RESPONSES_FOLDER, f"{user}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            responses = json.load(f)
        if 0 <= index < len(responses):
            responses.pop(index)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(responses, f, ensure_ascii=False, indent=2)
            return 'OK'
    return 'Not Found', 404

# אנשי קשר - טעינה
@app.route('/contacts', methods=['GET'])
def get_contacts():
    user = request.args.get('user')
    filepath = os.path.join(CONTACTS_FOLDER, f"{user}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify([])

# אנשי קשר - שמירה
@app.route('/contacts', methods=['POST'])
def save_contact():
    user = request.args.get('user')
    filepath = os.path.join(CONTACTS_FOLDER, f"{user}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            contacts = json.load(f)
    else:
        contacts = []
    new_contact = request.json
    contacts.append(new_contact)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)
    return 'OK'

# אנשי קשר - מחיקה
@app.route('/contacts', methods=['DELETE'])
def delete_contact():
    user = request.args.get('user')
    index = int(request.args.get('index'))
    filepath = os.path.join(CONTACTS_FOLDER, f"{user}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            contacts = json.load(f)
        if 0 <= index < len(contacts):
            contacts.pop(index)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(contacts, f, ensure_ascii=False, indent=2)
            return 'OK'
    return 'Not Found', 404
# קבוצות - טעינה
@app.route('/groups', methods=['GET'])
def get_groups():
    user = request.args.get('user')
    filepath = os.path.join(GROUPS_FOLDER, f"{user}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify({})

# קבוצות - שמירה
@app.route('/groups', methods=['POST'])
def save_group():
    user = request.args.get('user')
    filepath = os.path.join(GROUPS_FOLDER, f"{user}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            groups = json.load(f)
    else:
        groups = {}
    new_group = request.json
    group_name = new_group.get('group')
    phones = new_group.get('phones', [])
    if group_name:
        groups[group_name] = phones
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(groups, f, ensure_ascii=False, indent=2)
    return 'OK'

# מנהלים - טעינה
@app.route('/managers', methods=['GET'])
def get_managers():
    return jsonify(load_managers())

# מנהלים - שמירה
@app.route('/managers', methods=['POST'])
def save_manager():
    managers = load_managers()
    new_manager = request.json.get('phone')
    if new_manager and new_manager not in managers:
        managers.append(new_manager)
        save_managers(managers)
    return 'OK'

# שליחת SMS אמיתית ל-Inforu
@app.route('/send_sms', methods=['POST'])
def send_sms():
    data = request.json
    users = load_users()
    user = data.get('user')
    numbers = data.get('numbers', [])
    message = data.get('message')

    if not user or user not in users:
        return "Unauthorized", 401

    user_data = users[user]
    sender = user_data.get('sender')
    username = user
    password = user_data.get('password')

    # הכנת תוכן XML לשליחה ל-Inforu
    to_numbers = "".join(f"<PhoneNumber>{n}</PhoneNumber>" for n in numbers)

    xml_data = f"""<?xml version="1.0" encoding="utf-8"?>
<Inforu>
    <User>
        <Username>{username}</Username>
        <Password>{password}</Password>
    </User>
    <Content Type="sms">
        <Message>{message}</Message>
    </Content>
    <Recipients>
        {to_numbers}
    </Recipients>
    <Settings>
        <Sender>{sender}</Sender>
    </Settings>
</Inforu>"""

    headers = {'Content-Type': 'application/xml; charset=utf-8'}
    response = requests.post(INFORU_URL, data=xml_data.encode('utf-8'), headers=headers)

    if response.status_code == 200:
        return "OK"
    else:
        return "Error", 500
# טיפול בהודעות נכנסות מהטלפון (API דמה - אפשר להתחבר ל-Inforu לקבלת Webhook אמיתי)
@app.route('/incoming', methods=['POST'])
def incoming_sms():
    data = request.json
    from_number = data.get('from')
    message = data.get('message')
    
    managers = load_managers()
    if from_number not in managers:
        return "Unauthorized", 401

    # שלב ראשון: אם מגיעה הודעה רגילה -> שולחים למנהל שאלה
    user = find_user_by_manager(from_number)
    if not user:
        return "No user", 404

    # טוענים קבוצות
    groups_path = os.path.join(GROUPS_FOLDER, f"{user}.json")
    if not os.path.exists(groups_path):
        return "No groups", 404

    with open(groups_path, 'r', encoding='utf-8') as f:
        user_groups = json.load(f)

    # שמירת ההודעה האחרונה באופן זמני בקובץ
    temp_file = os.path.join(DATA_FOLDER, f"{from_number}_temp.json")
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump({"user": user, "message": message, "groups": list(user_groups.keys())}, f, ensure_ascii=False)

    # מחזירים לו שאלה: "לאיזו קבוצה לשלוח?"
    group_list = "\n".join([f"{i+1}. {g}" for i, g in enumerate
