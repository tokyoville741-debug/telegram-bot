import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=data)

@app.route("/")
def home():
    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    print(data)  # voir message dans logs

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text","")

    if text == "/start":
        send_message(chat_id, "Bot actif ✅")
    else:
        send_message(chat_id, "Message reçu: " + text)

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0", port=port)
