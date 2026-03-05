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

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
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
        "🚀 Welcome to OpenClaw AI\n\nChoose an option below 👇",
        reply_markup=markup
    )


@bot.message_handler(func=lambda m: m.text == "📚 Learn Binance Products")
def learn_products(message):
    bot.send_message(
        message.chat.id,
        "📚 Binance Products Overview:\n\n"
        "🔹 Spot Trading\n"
        "🔹 Futures\n"
        "🔹 Earn\n"
        "🔹 Staking"
    )


@bot.message_handler(func=lambda m: m.text == "🧠 Take a Crypto Quiz")
def crypto_quiz(message):
    bot.send_message(
        message.chat.id,
        "What is a Rollup?\n\n"
        "A) Layer 2 scaling solution\n"
        "B) Crypto wallet\n"
        "C) Exchange\n\n"
        "Type A, B, or C."
    )


@bot.message_handler(func=lambda m: m.text in ["A", "B", "C"])
def quiz_answer(message):
    if message.text == "A":
        bot.send_message(message.chat.id, "Correct! 🎉")
    else:
        bot.send_message(message.chat.id, "Wrong. The answer is A.")


# ==============================
# AI RESPONSE FUNCTION
# ==============================

def generate_ai_response(user_message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a crypto education assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300
        )

        return response.choices[0].message.content

    except Exception as e:
        print("OPENAI ERROR:", e)
        return "⚠️ AI connection error."


@bot.message_handler(func=lambda m: True)
def handle_ai(message):
    reply = generate_ai_response(message.text)
    bot.reply_to(message, reply)


# ==============================
# WEBHOOK ROUTE
# ==============================

@app.route("/", methods=["POST"])
def telegram_webhook():
    if request.headers.get("content-type") == "application/json":
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK", 200
    return "Forbidden", 403


@app.route("/", methods=["GET"])
def health_check():
    return "Bot is running!", 200
