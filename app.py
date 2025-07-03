from flask import Flask, request, session, redirect, url_for, render_template_string, jsonify
import requests
import json
import uuid

app = Flask(__name__)
app.secret_key = 'secretkey123'

API_URL = "                                            "
AUTH_HEADER = "Basic MjJ1cml5YTIyOjRkNTFjZGU5LTBkZmQtNGYwYi1iOTY4LWQ5MTA0NjdjZmM4MQ=="
SENDER = "0001"

# בסיס נתונים פשוט בזיכרון
users = {}  # username -> {"password": str, "contacts": list of dict, "codes": dict}
sessions = {}  # session_id -> username

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "שם משתמש כבר קיים"
        users[username] = {"password": password, "contacts": [], "codes": {}}
        return redirect(url_for('login'))
    return '''
        <form method="post">
            שם משתמש: <input name="username"><br>
            סיסמה: <input name="password" type="password"><br>
            <input type="submit" value="הרשם">
        </form>
    '''

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        return "פרטי התחברות שגויים"
    return '''
        <form method="post">
            שם משתמש: <input name="username"><br>
            סיסמה: <input name="password" type="password"><br>
            <input type="submit" value="התחבר">
        </form>
    '''

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    user = users[username]

    if request.method == "POST":
        phone = request.form['phone']
        name = request.form.get('name', '')
        notes = request.form.get('notes', '')
        user['contacts'].append({"phone": phone, "name": name, "notes": notes, "status": None})

    contact_list = "<ul>" + "".join([
        f"<li>{c['phone']} - {c.get('name', '')} - {c.get('notes', '')} - {c['status']}</li>"
        for c in user['contacts']
    ]) + "</ul>"

    return f'''
        <h1>ברוך הבא, {username}</h1>
        <form method="post">
            מספר טלפון: <input name="phone"><br>
            שם איש קשר: <input name="name"><br>
            הערות: <input name="notes"><br>
            <input type="submit" value="הוסף איש קשר">
        </form>
        <h2>רשימת אנשי קשר:</h2>
        {contact_list}
    '''

@app.route("/api/send_next", methods=["POST"])
def send_next():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if username not in users or users[username]['password'] != password:
        return jsonify({"error": "גישה נדחתה"})

    for contact in users[username]['contacts']:
        if contact['status'] is None:
            message = f"התקשר ל: {contact['phone']}\nשם: {contact.get('name', '')}\nהערות: {contact.get('notes', '')}"
            sms_data = {
                "Sender": SENDER,
                "Message": message,
                "Recipients": [{"Phone": data.get("to_phone")}]
            }
            headers = {
                "Content-Type": "application/json; charset=utf-8",
                "Authorization": AUTH_HEADER
            }
            try:
                requests.post(API_URL, headers=headers, json=sms_data)
                return jsonify({"status": "נשלח", "details": contact})
            except Exception as e:
                return jsonify({"error": str(e)})
    return jsonify({"status": "אין אנשי קשר פנויים"})

@app.route("/api/response", methods=["POST"])
def receive_response():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    digit = data.get("digit")

    if username not in users or users[username]['password'] != password:
        return jsonify({"error": "גישה נדחתה"})

    for contact in users[username]['contacts']:
        if contact['status'] is None:
            contact['status'] = digit
            return jsonify({"status": "עודכן", "contact": contact})

    return jsonify({"status": "לא נמצא איש קשר לעדכון"})

if __name__ == "__main__":
    app.run(debug=True)
