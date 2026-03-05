from flask import Flask, request
import telebot
from openai import OpenAI
import os

# ==============================
# CONFIGURATION
# ==============================

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

client = OpenAI(
    api_key=OPENAI_API_KEY
)

app = Flask(__name__)

# ==============================
# PAGE TEST
# ==============================

@app.route("/", methods=["GET"])
def home():
    return "OpenClaw AI Coach Bot actif 🚀"

# ==============================
# WEBHOOK TELEGRAM
# ==============================

@app.route("/", methods=["POST"])
def webhook():
    json_string = request.stream.read().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK", 200


# ==============================
# COMMANDE START
# ==============================

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "👋 Bonjour ! Je suis OpenClaw AI Coach.\n\nPose moi une question et je te répondrai avec l'IA."
    )


# ==============================
# IA CHAT
# ==============================

@bot.message_handler(func=lambda message: True)
def ai_chat(message):

    user_message = message.text

    try:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un assistant intelligent, utile et précis."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=500
        )

        reply = response.choices[0].message.content

        bot.reply_to(message, reply)

    except Exception as e:

        bot.reply_to(message, "❌ Erreur IA : " + str(e))


# ==============================
# LANCEMENT
# ==============================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
