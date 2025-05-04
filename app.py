# קובץ app.py משודרג לפי כל מה שבוצע בדשבורד

from flask import Flask, request, jsonify, send_from_directory
import json
import os
import requests
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

DATA_FOLDER = 'data'
RESPONSES_FOLDER = os.path.join(DATA_FOLDER, 'responses')
CONTACTS_FOLDER = os.path.join(DATA_FOLDER, 'contacts')
GROUPS_FOLDER = os.path.join(DATA_FOLDER, 'groups')
HISTORY_FILE = os.path.join(DATA_FOLDER, 'history.json')
STATS_FILE = os.path.join(DATA_FOLDER, 'stats.json')
USERS_FILE = os.path.join(DATA_FOLDER, 'users.json')
INFORU_URL = "https://uapi.inforu.co.il/SendMessageXml.ashx"

for folder in [DATA_FOLDER, RESPONSES_FOLDER, CONTACTS_FOLDER, GROUPS_FOLDER]:
    os.makedirs(folder, exist_ok=True)

scheduler = BackgroundScheduler()
scheduler.start()


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_stats(data):
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def append_history(entry):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
    history.insert(0, entry)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history[:100], f, ensure_ascii=False, indent=2)


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


@app.route('/send_now', methods=['POST'])
def send_now():
    data = request.json
    users = load_users()
    user = data.get('user')
    message = data.get('message')
    numbers = data.get('numbers', [])

    if not user or user not in users:
        return "Unauthorized", 401

    user_data = users[user]
    xml_data = f"""<?xml version="1.0" encoding="utf-8"?>
<Inforu>
  <User>
    <Username>{user}</Username>
    <Password>{user_data['password']}</Password>
  </User>
  <Content Type="sms">
    <Message>{message}</Message>
  </Content>
  <Recipients>
    {''.join(f'<PhoneNumber>{n}</PhoneNumber>' for n in numbers)}
  </Recipients>
  <Settings>
    <Sender>{user_data['sender']}</Sender>
  </Settings>
</Inforu>"""

    headers = {'Content-Type': 'application/xml; charset=utf-8'}
    response = requests.post(INFORU_URL, data=xml_data.encode('utf-8'), headers=headers)

    if response.status_code == 200:
        append_history({
            "user": user,
            "message": message,
            "numbers": numbers,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        stats = load_stats()
        stats.append({
            "user": user,
            "count": len(numbers),
            "time": datetime.now().strftime("%Y-%m-%d")
        })
        save_stats(stats)
        return "OK"
    return "Error", 500


@app.route('/history', methods=['GET'])
def get_history():
    user = request.args.get('user')
    history = load_history()
    filtered = [h for h in history if h['user'] == user]
    return jsonify(filtered)


@app.route('/stats', methods=['GET'])
def get_stats():
    user = request.args.get('user')
    stats = load_stats()
    daily = {}
    for s in stats:
        if s['user'] == user:
            day = s['time']
            daily[day] = daily.get(day, 0) + s['count']
    return jsonify({k: {'total': v} for k, v in daily.items()})


@app.route('/contacts')
def get_contacts():
    user = request.args.get('user')
    filepath = os.path.join(CONTACTS_FOLDER, f"{user}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify([])


@app.route('/groups')
def get_groups():
    user = request.args.get('user')
    filepath = os.path.join(GROUPS_FOLDER, f"{user}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify({})


@app.route('/responses')
def get_responses():
    user = request.args.get('user')
    filepath = os.path.join(RESPONSES_FOLDER, f"{user}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify([])


@app.route('/logout')
def logout():
    return "OK"


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/dashboard')
def dashboard():
    return send_from_directory('.', 'dashboard.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
