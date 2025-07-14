from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
AUTHORIZED_USER_ID = os.getenv("AUTHORIZED_USER_ID")  # Optional: Telegram user ID as string


@app.route('/')
def home():
    return "Telegram Bot Server is Running"


@app.route('/trend.json')
def get_trend():
    if os.path.exists("trend.json"):
        with open("trend.json", "r") as f:
            return f.read(), 200, {'Content-Type': 'application/json'}
    # Return default if no file found
    return jsonify({"trend": "NoTrend"}), 200


@app.route(f"/bot/{BOT_TOKEN}", methods=["POST"])
def receive_telegram():
    data = request.get_json()
    print("Received Telegram message:", data)

    # Authorization check (optional)
    if AUTHORIZED_USER_ID:
        user_id = str(data.get("message", {}).get("from", {}).get("id", ""))
        if user_id != AUTHORIZED_USER_ID:
            print(f"Unauthorized user {user_id} tried to send command.")
            return "Unauthorized", 403

    text = data.get("message", {}).get("text", "")
    if text.startswith("/trend"):
        parts = text.split(" ")
        if len(parts) == 2:
            trend = parts[1]
            with open("trend.json", "w") as f:
                json.dump({"trend": trend}, f)
            print(f"Updated trend.json to: {trend}")
            return "Trend updated", 200

    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"Starting Flask app on port {port}")
    app.run(host="0.0.0.0", port=port)

