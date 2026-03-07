import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"


def send_message(chat_id, text):
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)


# BTC price
def get_btc_price():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        r = requests.get(url)
        data = r.json()
        return data["price"]
    except Exception:
        return "Error"


@app.route("/", methods=["GET"])
def home():
    return "Bot running"


@app.route("/", methods=["POST"])
def webhook():

    data = request.get_json()

    if not data:
        return "ok"

    if "message" not in data:
        return "ok"

    message = data["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    # START
    if text == "/start":
        send_message(
            chat_id,
            "🤖 OpenClaw AI Crypto Bot\n\n"
            "Commands:\n"
            "/price\n"
            "/signal\n"
            "/portfolio\n"
            "/learn\n"
            "/trading\n"
            "/risk\n"
            "/market\n"
            "/dca\n"
            "/binance\n"
            "/help"
        )

    # HELP
    elif text == "/help":
        send_message(
            chat_id,
            "Bot Commands:\n"
            "/price\n"
            "/signal\n"
            "/portfolio\n"
            "/learn\n"
            "/trading\n"
            "/risk\n"
            "/market\n"
            "/dca\n"
            "/binance"
        )

    # PRICE
    elif text == "/price":
        price = get_btc_price()
        send_message(chat_id, f"💰 BTC Price: ${price}")

    # SIGNAL
    elif text == "/signal":
        send_message(
            chat_id,
            "📊 BTC Signal\n\n"
            "Trend: Bullish\n"
            "Strategy: Buy dips"
        )

    # PORTFOLIO
    elif text == "/portfolio":
        send_message(
            chat_id,
            "📊 Example Portfolio\n\n"
            "BTC 50%\n"
            "ETH 30%\n"
            "ALT 20%"
        )

    # LEARN
    elif text == "/learn":
        send_message(
            chat_id,
            "📚 Learn Crypto\n\n"
            "• Blockchain basics\n"
            "• What is Bitcoin\n"
            "• Risk management"
        )

    # TRADING
    elif text == "/trading":
        send_message(
            chat_id,
            "📈 Trading Tips\n\n"
            "• Follow trend\n"
            "• Use stop loss\n"
            "• Manage risk"
        )

    # RISK
    elif text == "/risk":
        send_message(
            chat_id,
            "⚠️ Risk Management\n\n"
            "Never risk more than 2% per trade."
        )

    # MARKET
    elif text == "/market":
        send_message(
            chat_id,
            "🌍 Market Insight\n\n"
            "Crypto market is volatile."
        )

    # DCA
    elif text == "/dca":
        send_message(
            chat_id,
            "💰 DCA Strategy\n\n"
            "Invest small amounts regularly."
        )

    # BINANCE
    elif text == "/binance":
        send_message(
            chat_id,
            "🟡 Trade crypto safely on Binance."
        )

    else:
        send_message(chat_id, "Unknown command")

    return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
