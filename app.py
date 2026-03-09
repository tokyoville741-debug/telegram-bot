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

    requests.post(url, json=payload)


def send_photo(chat_id, url, caption=None, keyboard=None):

    url_api = f"{TELEGRAM_API}/sendPhoto"

    payload = {
        "chat_id": chat_id,
        "photo": url,
        "caption": caption or ""
    }

    if keyboard:
        payload["reply_markup"] = {
            "keyboard": keyboard,
            "resize_keyboard": True
        }

    requests.post(url_api, json=payload)

# ---------------- MAIN MENU ----------------

main_menu = [
    ["📚 Learn", "📈 Trading"],
    ["⚠ Risk", "📊 Market"],
    ["💰 Price", "🧠 AI Assistant"],
    ["🌕 Altcoins", "🔒 Staking"],
    ["💼 Portfolio", "📰 News"]
]

# ---------------- SUB MENUS ----------------

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

# ---------------- AI ASSISTANT ----------------

def ai_answer(question):

    question = question.lower()

    if "bitcoin" in question:
        return "Bitcoin is the leading cryptocurrency and often drives the entire market."

    if "altcoin" in question:
        return "Altcoins usually perform well when Bitcoin stabilizes."

    if "trading" in question:
        return "Successful trading requires discipline, risk management and strategy."

    return "AI analysis: diversify your investments and follow market trends."

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return "Bot running"


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    if not data:
        return jsonify({"ok": True})

    message = data.get("message")

    if not message:
        return jsonify({"ok": True})

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

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

# ---------------- LEARN ----------------

    elif text == "What is Blockchain":
        send_message(chat_id,"Blockchain is a decentralized ledger that records transactions securely.",learn_menu)

    elif text == "Bitcoin Basics":
        send_message(chat_id,"Bitcoin is the first decentralized cryptocurrency created in 2009.",learn_menu)

    elif text == "Trading Psychology":
        send_message(chat_id,"Control fear and greed to become a successful trader.",learn_menu)

    elif text == "Market Cycles":
        send_message(chat_id,"Markets go through accumulation, bull run, distribution and bear market.",learn_menu)

# ---------------- TRADING ----------------

    elif text == "Day Trading":
        send_message(chat_id,"Day trading involves opening and closing trades in the same day.",trading_menu)

    elif text == "Swing Trading":
        send_message(chat_id,"Swing trading holds positions for days or weeks.",trading_menu)

    elif text == "Long Term Investing":
        send_message(chat_id,"Long-term investors hold assets for years.",trading_menu)

# ---------------- RISK ----------------

    elif text == "Stop Loss":
        send_message(chat_id,"A stop loss automatically closes a trade to limit losses.",risk_menu)

    elif text == "Position Size":
        send_message(chat_id,"Never risk more than 1-2% of your capital per trade.",risk_menu)

    elif text == "Risk Reward":
        send_message(chat_id,"Good traders aim for at least 1:2 risk reward ratio.",risk_menu)

# ---------------- MARKET ----------------

    elif text == "Market Cap":
        send_message(chat_id,"Market cap is price × circulating supply.",market_menu)

    elif text == "BTC Dominance":
        send_message(chat_id,"BTC dominance shows Bitcoin's share of the total crypto market.",market_menu)

    elif text == "Trading Volume":
        send_message(chat_id,"Trading volume shows how much of a coin is traded.",market_menu)

# ---------------- PRICE ----------------

    elif text == "BTC Price":
        send_message(chat_id,f"BTC = ${get_price('bitcoin')}",price_menu)

    elif text == "ETH Price":
        send_message(chat_id,f"ETH = ${get_price('ethereum')}",price_menu)

    elif text == "SOL Price":
        send_message(chat_id,f"SOL = ${get_price('solana')}",price_menu)

    elif text == "Top 5 Prices":
        send_message(chat_id,get_top_prices(),price_menu)

# ---------------- ALTCOINS ----------------

    elif text == "Top Altcoins":
        send_message(chat_id,"Popular altcoins: Ethereum, Solana, Cardano, Avalanche.",altcoin_menu)

    elif text == "Altcoin Season":
        send_message(chat_id,"Altcoin season happens when altcoins outperform Bitcoin.",altcoin_menu)

# ---------------- STAKING ----------------

    elif text == "What is Staking":
        send_message(chat_id,"Staking allows you to earn rewards by locking coins.",staking_menu)

    elif text == "Best Staking Coins":
        send_message(chat_id,"Popular staking coins: ETH, ADA, SOL.",staking_menu)

# ---------------- PORTFOLIO ----------------

    elif text == "Portfolio Strategy":
        send_message(chat_id,"Diversify between BTC, ETH and altcoins.",portfolio_menu)

    elif text == "Portfolio Example":
        send_message(chat_id,"Example: 50% BTC, 30% ETH, 20% Altcoins.",portfolio_menu)

# ---------------- NEWS ----------------

    elif text == "Latest News":
        send_message(chat_id,get_news(),news_menu)

# ---------------- AI ----------------

    elif text == "Market Prediction":
        send_message(chat_id,"AI predicts long-term growth for crypto adoption.",ai_menu)

    elif text == "Ask AI":
        send_message(chat_id,"Send your question about crypto.",ai_menu)

# ---------------- BACK ----------------

    elif text == "⬅ Back":
        send_message(chat_id,"Main Menu",main_menu)

# ---------------- AI FREE QUESTION ----------------

    else:

        answer = ai_answer(text)

        send_message(chat_id,answer,main_menu)

    return jsonify({"ok": True})


if __name__ == "__main__":

    port = int(os.environ.get("PORT",10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
