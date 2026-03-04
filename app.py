import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🚀 Welcome to my Binance Challenge Bot!\n\nThis bot is live and hosted online.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "✅ Bot is running successfully!")

bot.infinity_polling()
