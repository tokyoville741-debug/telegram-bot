from flask import Flask, request
import requests
import os

app = Flask(__name__)

# ==============================
# CONFIG
# ==============================

GROQ_API_KEY = "TA_CLE_GROQ"
TELEGRAM_TOKEN = "TON_TOKEN_TELEGRAM"

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

@app.route("/", methods=["POST"])
def webhook():

    data = request.get_json()

    if "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    user_message = data["message"].get("text", "")

    if not user_message:
        return "ok"

    try:

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "Tu es un assistant intelligent et utile."},
                    {"role": "user", "content": user_message}
                ]
            }
        )

        reply = response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        reply = "Erreur IA : " + str(e)

    requests.post(TELEGRAM_API, json={
        "chat_id": chat_id,
        "text": reply
    })

    return "ok"

# ==============================
# LANCEMENT
# ==============================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
