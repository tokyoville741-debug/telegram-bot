import telebot
from telebot import types
import os
from openai import OpenAI
from flask import Flask, request

# ==============================
# CONFIG
# ==============================

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ==============================
# TELEGRAM COMMANDS
# ==============================

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📚 Learn Binance Products")
    btn2 = types.KeyboardButton("🧠 Take a Crypto Quiz")
    btn3 = types.KeyboardButton("🚀 Explore Binance")
    markup.add(btn1, btn2, btn3)

    bot.send_message(
        message.chat.id,
        "🚀 Welcome to OpenClaw AI\n\n"
        "Your intelligent assistant for the Binance ecosystem.\n\n"
        "Choose an option below 👇",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == "📚 Learn Binance Products")
def learn_products(message):
    bot.send_message(
        message.chat.id,
        "📚 Binance Products Overview:\n\n"
        "🔹 Spot Trading – Buy and sell crypto instantly.\n"
        "🔹 Futures – Trade with leverage.\n"
        "🔹 Earn – Passive income products.\n"
        "🔹 Staking – Earn rewards by locking assets."
    )


@bot.message_handler(func=lambda message: message.text == "🧠 Take a Crypto Quiz")
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


@bot.message_handler(func=lambda message: message.text in ["A", "B", "C"])
def quiz_answer(message):
    if message.text == "A":
        bot.send_message(message.chat.id, "✅ Correct! A Rollup is a Layer 2 scaling solution.")
    else:
        bot.send_message(message.chat.id, "❌ Not quite. The correct answer is A.")


@bot.message_handler(func=lambda message: message.text == "🚀 Explore Binance")
def explore_binance(message):
    bot.send_message(
        message.chat.id,
        "🚀 Explore Binance:\n\n"
        "Visit Binance official website:\n"
        "https://www.binance.com"
    )


# ==============================
# AI RESPONSE HANDLER
# ==============================

@bot.message_handler(func=lambda message: True)
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
        print(e)
        bot.reply_to(message, "⚠️ Error connecting to AI.")


# ==============================
# FLASK ROUTES
# ==============================

@app.route('/', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200


@app.route('/')
def home():
    return "Bot is running!"


# ==============================
# START SERVER
# ==============================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 10000)))
