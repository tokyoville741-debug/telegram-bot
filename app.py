import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"


def send_message(chat_id, text):
    requests.post(TELEGRAM_URL, json={
        "chat_id": chat_id,
        "text": text
    })


def ask_groq(prompt):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    r = requests.post(url, headers=headers, json=data)

    return r.json()["choices"][0]["message"]["content"]


def get_price(symbol):

    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"

    r = requests.get(url)

    if r.status_code == 200:
        return r.json()["price"]
    else:
        return None


@app.route("/", methods=["GET"])
def home():
    return "Bot running"


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    message = data["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text.startswith("/start"):

        send_message(chat_id,
        "Welcome to OpenClaw AI Crypto Assistant.\n\n"
        "Use /help to see available commands.")

    elif text.startswith("/help"):

        help_text = """
Available commands:

/price BTC
/market
/signal BTC
/risk BTC
/dca BTC
/portfolio 1000
/sentiment BTC
/learn blockchain
/binance
"""

        send_message(chat_id, help_text)

    elif text.startswith("/price"):

        coin = text.split(" ")[1].upper()

        price = get_price(coin)

        if price:
            send_message(chat_id, f"{coin} price: ${price}")
        else:
            send_message(chat_id, "Coin not found")

    elif text.startswith("/market"):

        prompt = "Give a short overview of the crypto market today."

        response = ask_groq(prompt)

        send_message(chat_id, response)

    elif text.startswith("/signal"):

        coin = text.split(" ")[1]

        prompt = f"Give a trading signal for {coin}. Include trend and short explanation."

        response = ask_groq(prompt)

        send_message(chat_id, response)

    elif text.startswith("/risk"):

        coin = text.split(" ")[1]

        prompt = f"Explain risk management when trading {coin}."

        response = ask_groq(prompt)

        send_message(chat_id, response)

    elif text.startswith("/dca"):

        coin = text.split(" ")[1]

        prompt = f"Explain a DCA strategy for investing in {coin}."

        response = ask_groq(prompt)

        send_message(chat_id, response)

    elif text.startswith("/portfolio"):

        amount = text.split(" ")[1]

        prompt = f"Create a diversified crypto portfolio using ${amount} including BTC ETH BNB and one altcoin."

        response = ask_groq(prompt)

        send_message(chat_id, response)

    elif text.startswith("/sentiment"):

        coin = text.split(" ")[1]

        prompt = f"Give a short market sentiment analysis for {coin}. Is it bullish or bearish?"

        response = ask_groq(prompt)

        send_message(chat_id, response)

    elif text.startswith("/learn"):

        topic = text.replace("/learn ", "")

        prompt = f"Explain {topic} in simple terms for someone new to crypto."

        response = ask_groq(prompt)

        send_message(chat_id, response)

    elif text.startswith("/binance"):

        message = """
OpenClaw AI Assistant

Features:

Crypto price tracking
AI trading signals
Portfolio strategies
Risk management
Market sentiment
Crypto education

Built to enhance the Binance ecosystem.
"""

        send_message(chat_id, message)

    return "ok"
