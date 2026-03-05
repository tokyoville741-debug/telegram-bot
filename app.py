from flask import Flask, request
from openai import OpenAI
import requests
import os

app = Flask(__name__)

# =====================
# CONFIG
# =====================

OPENAI_API_KEY = "TA_CLE_OPENAI"
TELEGRAM_TOKEN = "TON_TOKEN_TELEGRAM"

client = OpenAI(api_key=OPENAI_API_KEY)

# =====================
# PAGE TEST
# =====================

@app.route("/")
def home():
    return "OpenClaw AI Coach Bot actif 🚀"


# =====================
# WEBHOOK TELEGRAM
# =====================

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    if "message" in data:

        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"].get("text", "")

        try:

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Tu es un assistant intelligent."},
                    {"role": "user", "content": user_message}
                ]
            )

            reply = response.choices[0].message.content

        except Exception as e:
            reply = "Erreur IA."

        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": reply
            }
        )

    return "ok"
