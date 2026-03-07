from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)


# BTC PRICE
def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url).json()
    price = response["bitcoin"]["usd"]
    return price


# SIMPLE SIGNAL
def get_signal():
    price = get_btc_price()

    if price < 60000:
        return f"BTC price ${price}\nSignal: BUY opportunity"
    elif price < 70000:
        return f"BTC price ${price}\nSignal: HOLD"
    else:
        return f"BTC price ${price}\nSignal: MARKET HOT - WAIT"


@app.route("/", methods=["POST"])
def webhook():

    data = request.get_json()

    if "message" in data:

        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        # START
        if text == "/start":
            send_message(chat_id,
            "Welcome to OpenClaw AI Coach\n\n"
            "Commands:\n"
            "/price - BTC price\n"
            "/signal - BTC signal\n"
            "/learn - crypto tips\n"
            "/portfolio - portfolio help"
            )

        # PRICE
        elif text == "/price":
            price = get_btc_price()
            send_message(chat_id, f"BTC price: ${price}")

        # SIGNAL
        elif text == "/signal":
            signal = get_signal()
            send_message(chat_id, signal)

        # LEARN
        elif text == "/learn":
            send_message(chat_id,
            "Crypto tips:\n\n"
            "1. Never invest money you need\n"
            "2. Use DCA strategy\n"
            "3. Avoid emotional trading\n"
            "4. Long term wins\n"
            )

        # PORTFOLIO
        elif text == "/portfolio":
            send_message(chat_id,
            "Portfolio tip:\n\n"
            "Example allocation:\n"
            "BTC 50%\n"
            "ETH 30%\n"
            "ALT 20%\n"
            )

    return "ok"


@app.route("/", methods=["GET"])
def home():
    return "Bot is running"
