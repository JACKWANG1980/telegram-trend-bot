from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN") or "default-token"  # Use a fallback for dev/testing
AUTHORIZED_USER_ID = os.getenv("AUTHORIZED_USER_ID")  # Optional: Telegram user ID as string

TREND_FILE = "trend.json"


@app.route('/')
def home():
    return "✅ Telegram Bot Server is Running"


from flask import send_file

@app.route('/trend.json')
def get_trend():
    if os.path.exists("trend.json"):
        return send_file("trend.json", mimetype="application/json")
    else:
        return jsonify({"trend": "NoTrend"}), 200


# Webhook route must exactly match what Telegram will POST to
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def receive_telegram():
    data = request.get_json()
    print("✅ Received Telegram message:", data)

    message = data.get("message", {})
    text = message.get("text", "")
    user_id = str(message.get("from", {}).get("id", ""))

    # Optional authorization
    if AUTHORIZED_USER_ID and user_id != AUTHORIZED_USER_ID:
        print(f"❌ Unauthorized user {user_id}")
        return "Unauthorized", 403

    if text.lower().startswith("/trend"):
        parts = text.strip().split(" ", 1)
        if len(parts) == 2:
            trend = parts[1]
            with open(TREND_FILE, "w") as f:
                json.dump({"trend": trend}, f)
            print(f"✅ trend.json updated to: {trend}")
            return "Trend updated", 200

    print("⚠️ Unrecognized command or wrong format.")
    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Starting Flask app on port {port}")
    app.run(host="0.0.0.0", port=port)
