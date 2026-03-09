import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ---------------- SEND FUNCTIONS ----------------

def send_message(chat_id, text, keyboard=None):

    url = f"{TELEGRAM_API}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    if keyboard:
        payload["reply_markup"] = {
            "keyboard": keyboard,
            "resize_keyboard": True
        }

    try:
        requests.post(url, json=payload)
    except:
        pass


# ---------------- MENUS ----------------

main_menu = [
    ["📚 Learn", "📈 Trading"],
    ["⚠ Risk", "📊 Market"],
    ["💰 Price", "🧠 AI Assistant"],
    ["🌕 Altcoins", "🔒 Staking"],
    ["💼 Portfolio", "📰 News"]
]

learn_menu = [
    ["What is Blockchain"],
    ["Bitcoin Basics"],
    ["Trading Psychology"],
    ["Market Cycles"],
    ["⬅ Back"]
]

trading_menu = [
    ["Day Trading"],
    ["Swing Trading"],
    ["Long Term Investing"],
    ["⬅ Back"]
]

risk_menu = [
    ["Stop Loss"],
    ["Position Size"],
    ["Risk Reward"],
    ["⬅ Back"]
]

market_menu = [
    ["Market Cap"],
    ["BTC Dominance"],
    ["Trading Volume"],
    ["⬅ Back"]
]

price_menu = [
    ["BTC Price", "ETH Price"],
    ["SOL Price", "Top 5 Prices"],
    ["⬅ Back"]
]

ai_menu = [
    ["Market Prediction"],
    ["Ask AI"],
    ["⬅ Back"]
]

altcoin_menu = [
    ["Top Altcoins"],
    ["Altcoin Season"],
    ["⬅ Back"]
]

staking_menu = [
    ["What is Staking"],
    ["Best Staking Coins"],
    ["⬅ Back"]
]

portfolio_menu = [
    ["Portfolio Strategy"],
    ["Portfolio Example"],
    ["⬅ Back"]
]

news_menu = [
    ["Latest News"],
    ["⬅ Back"]
]

# ---------------- API FUNCTIONS ----------------

def get_price(coin):

    try:

        url = "https://api.coingecko.com/api/v3/simple/price"

        params = {
            "ids": coin,
            "vs_currencies": "usd"
        }

        r = requests.get(url, params=params)
        data = r.json()

        return data[coin]["usd"]

    except:

        return "Unavailable"


def get_top_prices():

    try:

        url = "https://api.coingecko.com/api/v3/coins/markets"

        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 5,
            "page": 1
        }

        r = requests.get(url, params=params)
        data = r.json()

        text = "💰 <b>Top 5 Crypto Prices</b>\n\n"

        for coin in data:
            text += f"{coin['name']} : ${coin['current_price']}\n"

        return text

    except:

        return "Price data unavailable"


def get_news():

    try:

        url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"

        r = requests.get(url)
        data = r.json()

        text = "📰 <b>Latest Crypto News</b>\n\n"

        for n in data["Data"][:5]:
            text += f"{n['title']}\n{n['url']}\n\n"

        return text

    except:

        return "News unavailable"


# ---------------- AI FUNCTION ----------------

def ai_answer(question):

    if not question:
        return "Ask me something about crypto."

    q = question.lower()

    if "bitcoin" in q:
        return "Bitcoin is the first cryptocurrency and often drives the market."

    if "altcoin" in q:
        return "Altcoins usually move after Bitcoin stabilizes."

    if "trading" in q:
        return "Successful trading requires discipline and risk management."

    return "AI Insight: diversify your investments and follow market trends."


# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return "Bot running"


@app.route("/webhook", methods=["POST"])
def webhook():

    try:

        data = request.get_json()

        if not data:
            return jsonify({"ok": True})

        message = data.get("message")

        if not message:
            return jsonify({"ok": True})

        chat_id = message["chat"]["id"]
        text = message.get("text")

        if not text:
            return jsonify({"ok": True})

# ---------------- START ----------------

        if text == "/start":

            msg = """
🤖 <b>OpenClaw AI Coach</b>

Your Crypto Learning & AI Assistant.

📚 Learn crypto
📈 Trading strategies
⚠ Risk management
📊 Market knowledge
💰 Live crypto prices
🧠 AI market assistant
🌕 Altcoins insights
🔒 Staking guide
💼 Portfolio strategy
📰 Crypto news
"""

            send_message(chat_id, msg, main_menu)

# ---------------- MENU NAVIGATION ----------------

        elif text == "📚 Learn":
            send_message(chat_id, "📚 Crypto Education", learn_menu)

        elif text == "📈 Trading":
            send_message(chat_id, "📈 Trading Strategies", trading_menu)

        elif text == "⚠ Risk":
            send_message(chat_id, "⚠ Risk Management", risk_menu)

        elif text == "📊 Market":
            send_message(chat_id, "📊 Market Knowledge", market_menu)

        elif text == "💰 Price":
            send_message(chat_id, "💰 Crypto Prices", price_menu)

        elif text == "🧠 AI Assistant":
            send_message(chat_id, "🧠 AI Assistant", ai_menu)

        elif text == "🌕 Altcoins":
            send_message(chat_id, "🌕 Altcoins", altcoin_menu)

        elif text == "🔒 Staking":
            send_message(chat_id, "🔒 Staking", staking_menu)

        elif text == "💼 Portfolio":
            send_message(chat_id, "💼 Portfolio", portfolio_menu)

        elif text == "📰 News":
            send_message(chat_id, "📰 Crypto News", news_menu)

# ---------------- PRICE ----------------

        elif text == "BTC Price":
            send_message(chat_id, f"BTC = ${get_price('bitcoin')}", price_menu)

        elif text == "ETH Price":
            send_message(chat_id, f"ETH = ${get_price('ethereum')}", price_menu)

        elif text == "SOL Price":
            send_message(chat_id, f"SOL = ${get_price('solana')}", price_menu)

        elif text == "Top 5 Prices":
            send_message(chat_id, get_top_prices(), price_menu)

# ---------------- NEWS ----------------

        elif text == "Latest News":
            send_message(chat_id, get_news(), news_menu)

# ---------------- BACK ----------------

        elif text == "⬅ Back":
            send_message(chat_id, "Main Menu", main_menu)

# ---------------- AI FREE QUESTION ----------------

        else:

            answer = ai_answer(text)

            send_message(chat_id, answer, main_menu)

    except Exception as e:

        print("ERROR:", e)

    return jsonify({"ok": True})


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
)
