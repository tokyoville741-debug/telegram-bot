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
    try:
        requests.post(url, json=payload, timeout=5)
    except:
        pass


def get_btc_price():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        r = requests.get(url, timeout=5)
        data = r.json()
        return data.get("price", "Unavailable")
    except:
        return "Error fetching price"


@app.route("/", methods=["GET"])
def home():
    return "Bot running"


# TELEGRAM WEBHOOK
@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    if not data or "message" not in data:
        return "ok"

    message = data["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if not text:
        return "ok"

    text = text.split()[0]  # Fix commands like /start@botname

    if text.startswith("/start"):
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

    elif text == "/price":
        price = get_btc_price()
        send_message(chat_id, f"💰 BTC Price: ${price}")

    elif text == "/signal":
        send_message(chat_id, "📊 BTC Signal\n\nTrend: Bullish\nStrategy: Buy dips")

    elif text == "/portfolio":
        send_message(chat_id, "📊 Example Portfolio\nBTC 50%\nETH 30%\nALT 20%")

    elif text == "/learn":
        send_message(chat_id, "📚 Learn Crypto\n• Blockchain\n• Bitcoin\n• Risk")

    elif text == "/trading":
        send_message(chat_id, "📈 Trading Tips\n• Follow trend\n• Use stop loss")

    elif text == "/risk":
        send_message(chat_id, "⚠️ Never risk more than 2% per trade")

    elif text == "/market":
        send_message(chat_id, "🌍 Crypto market is volatile")

    elif text == "/dca":
        send_message(chat_id, "💰 DCA = invest regularly")

    elif text == "/binance":
        send_message(chat_id, "🟡 Trade safely on Binance")

    else:
        send_message(chat_id, "Unknown command")

    return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
