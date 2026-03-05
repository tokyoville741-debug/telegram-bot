from flask import Flask, request
from openai import OpenAI
import requests
import os

app = Flask(__name__)

# ==============================
# CONFIGURATION
# ==============================

OPENAI_API_KEY = "TA_CLE_OPENAI"
TELEGRAM_TOKEN = "TON_TOKEN_TELEGRAM"

client = OpenAI(api_key=OPENAI_API_KEY)

TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"


# ==============================
# PAGE TEST
# ==============================

@app.route("/", methods=["GET"])
def home():
    return "OpenClaw AI Coach Bot actif 🚀"


# ==============================
# WEBHOOK TELEGRAM
# ==============================

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    if "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    user_message = data["message"].get("text", "")

    try:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es un assistant intelligent, utile et précis."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500
        )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = "Erreur IA : " + str(e)

    requests.post(
        TELEGRAM_URL,
        json={
            "chat_id": chat_id,
            "text": reply
        }
    )

    return "ok"


# ==============================
# LANCEMENT SERVEUR
# ==============================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
