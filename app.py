from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
AUTHORIZED_USER_ID = os.getenv("AUTHORIZED_USER_ID")  # Optional security

@app.route('/')
def home():
    return "Telegram Bot Server is Running"

@app.route('/trend.json')
def get_trend():
    if os.path.exists("trend.json"):
        with open("trend.json", "r") as f:
            return f.read(), 200, {'Content-Type': 'application/json'}
    return jsonify({"trend": "NoTrend"}), 200

@app.route(f"/bot/{BOT_TOKEN}", methods=["POST"])
def receive_telegram():
    data = request.get_json()

    # Optional user filter
    if AUTHORIZED_USER_ID:
        if str(data["message"]["from"]["id"]) != AUTHORIZED_USER_ID:
            return "Unauthorized", 403

    text = data["message"].get("text", "")
    if text.startswith("/trend"):
        parts = text.split(" ")
        if len(parts) == 2:
            trend = parts[1]
            with open("trend.json", "w") as f:
                json.dump({"trend": trend}, f)
            return "Trend updated", 200
    return "OK", 200
