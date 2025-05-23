from flask import Flask, send_file, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='.', static_url_path='')

USERNAME = "023011196"
PASSWORD = "1234"
API_URL = "https://www.call2all.co.il/ym/api"
LISTENERS_FILE = "listeners.txt"
MINUTES_FILE = "minutes.txt"

from datetime import datetime, timedelta
today = datetime.utcnow().date()
yesterday = today - timedelta(days=1)
from_date = yesterday.isoformat()
to_date = today.isoformat()

def update_data():
    token = f"{USERNAME}:{PASSWORD}"

    # עדכון מספר מאזינים פעילים
    try:
        r = requests.get(f"{API_URL}/GetIncomingCalls?token={token}")
        data = r.json()
        if data.get("responseStatus") == "OK":
            count = data.get("callsCount", 0)
            with open(LISTENERS_FILE, "w") as f:
                f.write(str(count))
            print(f"✔ מספר מאזינים עודכן: {count}")
        else:
            print("❌ GetIncomingCalls:", data.get("message"))
    except Exception as e:
        print("❌ שגיאה ב־GetIncomingCalls:", e)

    # עדכון דקות שיחה
    try:
        r = requests.get(f"{API_URL}/GetIncomingSum?token={token}&fromDate={from_date}&toDate={to_date}")
        data = r.json()
        if data.get("responseStatus") == "OK":
            minutes = data.get("totalMinutes", 0)
            with open(MINUTES_FILE, "w") as f:
                f.write(str(minutes))
            print(f"✔ דקות שיחה עודכנו: {minutes}")
        else:
            print("❌ GetIncomingSum:", data.get("message"))
    except Exception as e:
        print("❌ שגיאה ב־GetIncomingSum:", e)

@app.route('/')
def home():
    update_data()
    return "OK"

@app.route('/listeners.txt')
def get_listeners():
    return send_file(LISTENERS_FILE) if os.path.exists(LISTENERS_FILE) else "0"

@app.route('/minutes.txt')
def get_minutes():
    return send_file(MINUTES_FILE) if os.path.exists(MINUTES_FILE) else "0"

@app.route('/dashboard')
def dashboard():
    return send_from_directory('.', 'index.html')
