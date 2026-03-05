from flask import Flask, request
import requests
from openai import OpenAI
import os

app = Flask(__name__)

# =========================
# CONFIG
# =========================

OPENAI_API_KEY = "TA_CLE_OPENAI"
TELEGRAM_TOKEN = "TON_TOKEN_TELEGRAM"

client = OpenAI(api_key=OPENAI_API_KEY)

# =========================
# PAGE HOME
# =========================

@app.route("/")
def home():
    return "OpenClaw AI Coach Bot actif 🚀"


# =========================
# WEBHOOK TELEGRAM
# =========================

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    if "message" in data:

        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"].get("text")

        if user_message:

            # Réponse IA
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Tu es OpenClaw AI Coach, un assistant intelligent, utile et clair."
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                max_tokens=500
            )

            reply = response.choices[0].message.content

            # Envoyer réponse à Telegram
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

            payload = {
                "chat_id": chat_id,
                "text": reply
            }

            requests.post(url, json=payload)

    return "ok"


# =========================
# RUN
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
