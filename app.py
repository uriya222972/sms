from flask import Flask, send_file, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='.', static_url_path='')

USERNAME = "0795905093"
PASSWORD = "1234"
API_URL = "https://www.call2all.co.il/ym/api/GetIncomingCalls"
OUTPUT_FILE = "listeners.txt"

def update_listeners():
    token = f"{USERNAME}:{PASSWORD}"
    url = f"{API_URL}?token={token}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("responseStatus") == "OK":
            count = data.get("callsCount", 0)
            with open(OUTPUT_FILE, "w") as f:
                f.write(str(count))
            print(f"✔ מספר מאזינים עודכן: {count}")
        else:
            print("❌ שגיאה מהשרת:", data.get("message", "לא ידוע"))
    except Exception as e:
        print("❌ שגיאה בבקשה:", e)

@app.route('/')
def home():
    update_listeners()
    return "OK"

@app.route('/listeners.txt')
def get_listeners():
    if os.path.exists(OUTPUT_FILE):
        return send_file(OUTPUT_FILE)
    return "0"

@app.route('/dashboard')
def dashboard():
    return send_from_directory('.', 'index.html')
