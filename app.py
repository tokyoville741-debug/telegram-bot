import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def send_message(chat_id, text):
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(TELEGRAM_API, json=payload)


# -------- BTC PRICE --------
def get_btc_price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        data = r.json()
        return data["price"]
    except:
        return "Error fetching price"


# -------- HOME ROUTE --------
@app.route("/", methods=["GET"])
def home():
    return "Bot running"


# -------- TELEGRAM WEBHOOK --------
@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    if not data or "message" not in data:
        return "ok"

    message = data["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    # START
    if text == "/start":
        send_message(chat_id,
        "🚀 Welcome to OpenClaw AI Coach\n\n"
        "Commands:\n"
        "/learn\n"
        "/trading\n"
        "/risk\n"
        "/market\n"
        "/price\n"
        "/signal\n"
        "/dca\n"
        "/portfolio\n"
        "/binance\n"
        "/help")

    # HELP
    elif text == "/help":
        send_message(chat_id,
        "Bot commands:\n"
        "/price - BTC price\n"
        "/signal - trading signal\n"
        "/portfolio - portfolio example\n"
        "/learn - crypto learning\n"
        "/trading - trading basics\n"
        "/risk - risk management\n"
        "/market - market insight\n"
        "/dca - DCA strategy\n"
        "/binance - Binance info")

    # PRICE
    elif text == "/price":
        price = get_btc_price()
        send_message(chat_id, f"💰 BTC Price: ${price}")

    # SIGNAL
    elif text == "/signal":
        send_message(chat_id,
        "📊 BTC Signal\n\n"
        "Trend: Bullish\n"
        "Strategy: Buy dips / Hold")

    # LEARN
    elif text == "/learn":
        send_message(chat_id,
        "📚 Crypto Learning\n\n"
        "• Blockchain basics\n"
        "• What is Bitcoin\n"
        "• How crypto works")

    # TRADING
    elif text == "/trading":
        send_message(chat_id,
        "📈 Trading Basics\n\n"
        "• Follow the trend\n"
        "• Use stop loss\n"
        "• Control emotions")

    # RISK
    elif text == "/risk":
        send_message(chat_id,
        "⚠️ Risk Management\n\n"
        "Never risk more than 1-2% per trade.")

    # MARKET
    elif text == "/market":
        send_message(chat_id,
        "🌎 Market Insight\n\n"
        "Crypto market is volatile.\n"
        "Always manage risk.")

    # DCA
    elif text == "/dca":
        send_message(chat_id,
        "💰 DCA Strategy\n\n"
        "Invest small amounts regularly.")

    # PORTFOLIO
    elif text == "/portfolio":
        send_message(chat_id,
        "📊 Portfolio Example\n\n"
        "BTC 50%\n"
        "ETH 30%\n"
        "ALT 20%")

    # BINANCE
    elif text == "/binance":
        send_message(chat_id,
        "🟡 Binance\n\n"
        "Trade crypto securely on Binance.")

    else:
        send_message(chat_id, "Unknown command")

    return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
