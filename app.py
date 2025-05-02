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
MANAGERS_FILE = os.path.join(DATA_FOLDER, 'managers.json')
USERS_FILE = os.path.join(DATA_FOLDER, 'users.json')
STATS_FILE = os.path.join(DATA_FOLDER, 'stats.json')

INFORU_URL = "https://uapi.inforu.co.il/SendMessageXml.ashx"

# ודא שתיקיות קיימות
for folder in [DATA_FOLDER, RESPONSES_FOLDER, CONTACTS_FOLDER, GROUPS_FOLDER]:
    os.makedirs(folder, exist_ok=True)

scheduler = BackgroundScheduler()
scheduler.start()

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def load_managers():
    if os.path.exists(MANAGERS_FILE):
        with open(MANAGERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_managers(managers):
    with open(MANAGERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(managers, f, ensure_ascii=False, indent=2)

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_stats(stats):
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def log_stat(user, numbers, message):
    stats = load_stats()
    stats.append({
        "user": user,
        "count": len(numbers),
        "message": message,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_stats(stats)

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
        log_stat(user, numbers, message)
        return "OK"
    return "Error", 500

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
