import telebot
from telebot import types
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📚 Learn Binance Products")
    btn2 = types.KeyboardButton("🧠 Take a Crypto Quiz")
    btn3 = types.KeyboardButton("🚀 Explore Binance")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)

    bot.send_message(
        message.chat.id,
        "🚀 Welcome to OpenClaw AI\n\n"
        "Your intelligent assistant for the Binance ecosystem.\n\n"
        "I help you:\n"
        "• Understand Binance products\n"
        "• Learn crypto fundamentals\n"
        "• Explore safely\n\n"
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
        "Visit Binance official website to discover all products and services:\n"
        "https://www.binance.com"
    )
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    from threading import Thread
    import os

    bot.remove_webhook()

    # Lancer le bot Telegram dans un thread séparé
    Thread(target=bot.infinity_polling).start()

    # Lancer Flask pour que Render détecte le port
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
