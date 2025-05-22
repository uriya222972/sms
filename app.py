from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'מערכת מאזינים פעילה'

@app.route('/update_listeners', methods=['POST'])
def update_listeners():
    count = request.data.decode('utf-8').strip()
    with open('listeners.txt', 'w') as f:
        f.write(count)
    return 'OK', 200

@app.route('/listeners.txt')
def get_listeners():
    if os.path.exists('listeners.txt'):
        return send_file('listeners.txt')
    return '0', 200

