import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    url = f"{TELEGRAM_API}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=data)

@app.route("/", methods=["GET"])
def home():
    return "Bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send_message(chat_id, "Bot actif ✅\n\nCommandes:\n/start\n/trading\n/risk")

        elif text == "/trading":
            send_message(chat_id,
            "Trading Basics 📊\n\n"
            "Important concepts:\n"
            "• Support and Resistance\n"
            "• Market Trends\n"
            "• Technical Indicators\n"
            "• Volume analysis\n\n"
            "Always trade with a plan and risk management.")

        elif text == "/risk":
            send_message(chat_id,
            "Risk Management ⚠️\n\n"
            "Golden rules:\n"
            "• Never risk more than 2% per trade\n"
            "• Always use stop-loss\n"
            "• Avoid emotional trading\n"
            "• Diversify your portfolio")

        else:
            send_message(chat_id, "Commande inconnue.")

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
