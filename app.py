from flask import Flask, request
import requests
import os
from groq import Groq

app = Flask(__name__)

# ==============================
# CONFIG
# ==============================

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

client = Groq(api_key=GROQ_API_KEY)

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"


# ==============================
# PAGE TEST
# ==============================

@app.route("/")
def home():
    return "OpenClaw AI Coach Bot actif 🚀"


# ==============================
# WEBHOOK TELEGRAM
# ==============================

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    if "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    user_message = data["message"].get("text", "")

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Tu es un assistant intelligent et utile."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = "Erreur IA : " + str(e)

    requests.post(TELEGRAM_API, json={
        "chat_id": chat_id,
        "text": reply
    })

    return "ok"


# ==============================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
