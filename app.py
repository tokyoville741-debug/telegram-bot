import os
import telebot
from telebot import types
from openai import OpenAI
from flask import Flask, request

# ==============================
# CONFIGURATION
# ==============================

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing")

client = OpenAI(api_key=OPENAI_API_KEY)

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ==============================
# TELEGRAM COMMANDS
# ==============================

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("📚 Learn Binance Products"),
        types.KeyboardButton("🧠 Take a Crypto Quiz"),
        types.KeyboardButton("🚀 Explore Binance")
    )

    bot.send_message(
        message.chat.id,
        "🚀 Welcome to OpenClaw AI\n\n"
        "Your intelligent assistant for the Binance ecosystem.\n\n"
        "Choose an option below 👇",
        reply_markup=markup
    )


@bot.message_handler(func=lambda m: m.text == "📚 Learn Binance Products")
def learn_products(message):
    bot.send_message(
        message.chat.id,
        "📚 Binance Products Overview:\n\n"
        "🔹 Spot Trading – Buy and sell crypto instantly.\n"
        "🔹 Futures – Trade with leverage.\n"
        "🔹 Earn – Passive income products.\n"
        "🔹 Staking – Earn rewards by locking assets."
    )


@bot.message_handler(func=lambda m: m.text == "🧠 Take a Crypto Quiz")
def crypto_quiz(message):
    bot.send_message(
        message.chat.id,
        "🧠 Quiz Time!\n\n"
        "What is a Rollup?\n\n"
        "A) Layer 2 scaling solution\n"
        "B) Crypto wallet\n"
        "C) Exchange\n\n"
        "Type A, B, or C."
    )


@bot.message_handler(func=lambda m: m.text in ["A", "B", "C"])
def quiz_answer(message):
    if message.text == "A":
        bot.send_message(message.chat.id, "✅ Correct! A Rollup is a Layer 2 scaling solution.")
    else:
        bot.send_message(message.chat.id, "❌ Not quite. The correct answer is A.")


@bot.message_handler(func=lambda m: m.text == "🚀 Explore Binance")
def explore_binance(message):
    bot.send_message(
        message.chat.id,
        "🚀 Explore Binance:\n\n"
        "Visit Binance official website:\n"
        "https://www.binance.com"
    )


# ==============================
# AI HANDLER
# ==============================

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are OpenClaw AI Coach specialized in Binance and crypto education."},
                {"role": "user", "content": message.text}
            ]
        )

        reply = response.choices[0].message.content
        bot.reply_to(message, reply)

    except Exception as e:
        print("OpenAI Error:", e)
        bot.reply_to(message, "⚠️ Error connecting to AI.")


# ==============================
# FLASK ROUTES (WEBHOOK)
# ==============================

@app.route("/", methods=["POST"])
def telegram_webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200


@app.route("/", methods=["GET"])
def health_check():
    return "Bot is running!", 200


# ==============================
# IMPORTANT FOR GUNICORN
# ==============================

# Ne PAS utiliser app.run() en production
# Gunicorn va automatiquement détecter "app"
