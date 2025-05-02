from flask import Flask, request, jsonify, send_from_directory
import json
import os
import requests
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# תיקיות שמירת קבצים
DATA_FOLDER = 'data'
RESPONSES_FOLDER = os.path.join(DATA_FOLDER, 'responses')
CONTACTS_FOLDER = os.path.join(DATA_FOLDER, 'contacts')
GROUPS_FOLDER = os.path.join(DATA_FOLDER, 'groups')
STATS_FOLDER = os.path.join(DATA_FOLDER, 'stats')
SCHEDULED_FOLDER = os.path.join(DATA_FOLDER, 'scheduled')
MANAGERS_FILE = os.path.join(DATA_FOLDER, 'managers.json')
USERS_FILE = os.path.join(DATA_FOLDER, 'users.json')

INFORU_URL = "https://uapi.inforu.co.il/SendMessageXml.ashx"

for folder in [DATA_FOLDER, RESPONSES_FOLDER, CONTACTS_FOLDER, GROUPS_FOLDER, STATS_FOLDER, SCHEDULED_FOLDER]:
    os.makedirs(folder, exist_ok=True)

scheduler = BackgroundScheduler()
scheduler.start()

def load_json_file(path, default):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default

def save_json_file(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_users():
    return load_json_file(USERS_FILE, {})

def save_users(users):
    save_json_file(USERS_FILE, users)

def load_managers():
    return load_json_file(MANAGERS_FILE, [])

def save_managers(managers):
    save_json_file(MANAGERS_FILE, managers)

def log_stats(user, count, group=None):
    date_str = datetime.now().strftime('%Y-%m-%d')
    stats_file = os.path.join(STATS_FOLDER, f"{user}.json")
    stats = load_json_file(stats_file, {})
    if date_str not in stats:
        stats[date_str] = {"total": 0, "groups": {}}
    stats[date_str]["total"] += count
    if group:
        stats[date_str]["groups"][group] = stats[date_str]["groups"].get(group, 0) + count
    save_json_file(stats_file, stats)

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

@app.route('/responses', methods=['GET', 'POST', 'DELETE'])
def handle_responses():
    user = request.args.get('user')
    filepath = os.path.join(RESPONSES_FOLDER, f"{user}.json")
    responses = load_json_file(filepath, [])
    if request.method == 'GET':
        return jsonify(responses)
    elif request.method == 'POST':
        responses.append(request.json)
        save_json_file(filepath, responses)
        return 'OK'
    elif request.method == 'DELETE':
        index = int(request.args.get('index'))
        if 0 <= index < len(responses):
            responses.pop(index)
            save_json_file(filepath, responses)
            return 'OK'
        return 'Not Found', 404

@app.route('/contacts', methods=['GET', 'POST', 'DELETE'])
def handle_contacts():
    user = request.args.get('user')
    filepath = os.path.join(CONTACTS_FOLDER, f"{user}.json")
    contacts = load_json_file(filepath, [])
    if request.method == 'GET':
        return jsonify(contacts)
    elif request.method == 'POST':
        contacts.append(request.json)
        save_json_file(filepath, contacts)
        return 'OK'
    elif request.method == 'DELETE':
        index = int(request.args.get('index'))
        if 0 <= index < len(contacts):
            contacts.pop(index)
            save_json_file(filepath, contacts)
            return 'OK'
        return 'Not Found', 404

@app.route('/groups', methods=['GET', 'POST'])
def handle_groups():
    user = request.args.get('user')
    filepath = os.path.join(GROUPS_FOLDER, f"{user}.json")
    groups = load_json_file(filepath, {})
    if request.method == 'GET':
        return jsonify(groups)
    elif request.method == 'POST':
        new_group = request.json
        group_name = new_group.get('group')
        phones = new_group.get('phones', [])
        if group_name:
            groups[group_name] = phones
            save_json_file(filepath, groups)
        return 'OK'

@app.route('/managers', methods=['GET', 'POST'])
def handle_managers():
    managers = load_managers()
    if request.method == 'GET':
        return jsonify(managers)
    elif request.method == 'POST':
        new_manager = request.json.get('phone')
        if new_manager and new_manager not in managers:
            managers.append(new_manager)
            save_managers(managers)
        return 'OK'

@app.route('/send_sms', methods=['POST'])
def send_sms():
    data = request.json
    users = load_users()
    user = data.get('user')
    numbers = data.get('numbers', [])
    message = data.get('message')
    delay_minutes = data.get('delay_minutes', 0)
    group = data.get('group')

    if not user or user not in users:
        return "Unauthorized", 401

    if delay_minutes > 0:
        send_time = datetime.now() + timedelta(minutes=delay_minutes)
        job_id = f"{user}_{datetime.now().timestamp()}"
        scheduler.add_job(func=send_bulk_sms, trigger='date', run_date=send_time,
                          args=[numbers, message, user, group], id=job_id)
        return f"Scheduled for {send_time.strftime('%Y-%m-%d %H:%M:%S')}"

    send_bulk_sms(numbers, message, user, group)
    return "OK"

@app.route('/stats', methods=['GET'])
def get_stats():
    user = request.args.get('user')
    stats_file = os.path.join(STATS_FOLDER, f"{user}.json")
    stats = load_json_file(stats_file, {})
    return jsonify(stats)

def send_bulk_sms(numbers, message, user, group=None):
    users = load_users()
    user_data = users.get(user)
    if not user_data:
        return

    numbers_xml = "".join(f"<PhoneNumber>{n}</PhoneNumber>" for n in numbers)
    xml_data = f"""<?xml version="1.0" encoding="utf-8"?>
<Inforu>
    <User>
        <Username>{user}</Username>
        <Password>{user_data.get('password')}</Password>
    </User>
    <Content Type="sms">
        <Message>{message}</Message>
    </Content>
    <Recipients>
        {numbers_xml}
    </Recipients>
    <Settings>
        <Sender>{user_data.get('sender')}</Sender>
    </Settings>
</Inforu>"""

    headers = {'Content-Type': 'application/xml; charset=utf-8'}
    requests.post(INFORU_URL, data=xml_data.encode('utf-8'), headers=headers)
    log_stats(user, len(numbers), group)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')
