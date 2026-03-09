import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Variables d'environnement
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL") + WEBHOOK_PATH

# Page d'accueil pour éviter erreur 404
@app.route("/")
def home():
    return "Bot is running"

# Webhook Telegram
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text","")

        if text == "/start":
            send_message(chat_id,"Hello 👋 Your bot is working!")

        else:
            send_message(chat_id,"I received: " + text)

    return "ok"

# Fonction envoyer message
def send_message(chat_id,text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }

    requests.post(url,json=payload)

# Setup webhook
@app.before_first_request
def setup_webhook():
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    requests.get(url,params={"url":WEBHOOK_URL})

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=10000)
