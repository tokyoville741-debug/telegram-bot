import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

user_state = {}

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
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print("Telegram send error:", e)

def send_photo(chat_id, photo_url, caption=None, keyboard=None):
    url = f"{TELEGRAM_API}/sendPhoto"

    payload = {
        "chat_id": chat_id,
        "photo": photo_url,
        "caption": caption if caption else ""
    }

    if keyboard:
        payload["reply_markup"] = {
            "keyboard": keyboard,
            "resize_keyboard": True
        }

    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print("Telegram photo error:", e)

main_menu = [
    ["📚 Learn", "📈 Trading"],
    ["⚠ Risk", "📊 Market"],
    ["💰 Price", "🧠 AI Analysis"],
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
    ["Scalping"],
    ["Day Trading"],
    ["Swing Trading"],
    ["Trend Trading"],
    ["⬅ Back"]
]

risk_menu = [
    ["Risk per trade"],
    ["Stop loss"],
    ["Position sizing"],
    ["⬅ Back"]
]

market_menu = [
    ["Bull Market"],
    ["Bear Market"],
    ["Market Sentiment"],
    ["⬅ Back"]
]

price_menu = [
    ["BTC Price"],
    ["ETH Price"],
    ["SOL Price"],
    ["📈 BTC Chart"],
    ["⬅ Back"]
]

ai_menu = [
    ["AI Market Analysis"],
    ["Trend Strength"],
    ["Volatility"],
    ["⬅ Back"]
]

altcoin_menu = [
    ["What are Altcoins"],
    ["Popular Altcoins"],
    ["⬅ Back"]
]

staking_menu = [
    ["What is Staking"],
    ["Staking Rewards"],
    ["⬅ Back"]
]

portfolio_menu = [
    ["Portfolio Diversification"],
    ["Long term strategy"],
    ["⬅ Back"]
]

news_menu = [
    ["Latest Crypto News"],
    ["⬅ Back"]
]

def get_crypto_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"

        params = {
            "ids": "bitcoin,ethereum,solana",
            "vs_currencies": "usd"
        }

        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        btc = data["bitcoin"]["usd"]
        eth = data["ethereum"]["usd"]
        sol = data["solana"]["usd"]

        return f"""
💰 Crypto Prices

BTC : ${btc}
ETH : ${eth}
SOL : ${sol}
"""

    except Exception as e:
        print("Price API error:", e)
        return "⚠ Unable to fetch prices."

def get_crypto_news():
    try:
        url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
        r = requests.get(url, timeout=10)
        data = r.json()

        news_list = data["Data"][:5]

        news_text = "📰 Latest Crypto News\n\n"

        for n in news_list:
            title = n["title"]
            link = n["url"]
            news_text += f"{title}\n{link}\n\n"

        return news_text

    except Exception as e:
        print("News API error:", e)
        return "⚠ Unable to fetch news."

@app.route("/")
def home():
    return "Bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    if not data:
        return jsonify({"status": "ok"}), 200

    message = data.get("message")

    if not message:
        return jsonify({"status": "ok"}), 200

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text in ["/start", "menu", "Menu"]:

        user_state[chat_id] = "main"

        reply = """
🤖 OpenClaw AI Coach

Welcome to the Crypto Learning Bot
Choose a section
"""

        send_message(chat_id, reply, main_menu)

    elif text == "📚 Learn":
        send_message(chat_id, "📚 Learn Crypto", learn_menu)

    elif text == "📈 Trading":
        send_message(chat_id, "📈 Trading Education", trading_menu)

    elif text == "⚠ Risk":
        send_message(chat_id, "⚠ Risk Management", risk_menu)

    elif text == "📊 Market":
        send_message(chat_id, "📊 Market Knowledge", market_menu)

    elif text == "💰 Price":
        send_message(chat_id, get_crypto_prices(), price_menu)

    elif text == "🧠 AI Analysis":
        send_message(chat_id, "AI tools", ai_menu)

    elif text == "🌕 Altcoins":
        send_message(chat_id, "Altcoins information", altcoin_menu)

    elif text == "🔒 Staking":
        send_message(chat_id, "Staking section", staking_menu)

    elif text == "💼 Portfolio":
        send_message(chat_id, "Portfolio management", portfolio_menu)

    elif text == "📰 News":
        send_message(chat_id, get_crypto_news(), news_menu)

    elif text == "What is Blockchain":
        send_message(chat_id, "Blockchain is a decentralized digital ledger that records transactions across many computers. It ensures transparency, security and immutability.", learn_menu)

    elif text == "Bitcoin Basics":
        send_message(chat_id, "Bitcoin is the first cryptocurrency created in 2009 by Satoshi Nakamoto. It allows peer to peer payments without banks.", learn_menu)

    elif text == "Trading Psychology":
        send_message(chat_id, "Trading psychology refers to the emotions that influence trading decisions such as fear and greed.", learn_menu)

    elif text == "Market Cycles":
        send_message(chat_id, "Markets move in cycles: accumulation, uptrend, distribution and downtrend.", learn_menu)

    elif text == "Scalping":
        send_message(chat_id, "Scalping is a fast strategy where traders make many small profits.", trading_menu)

    elif text == "Day Trading":
        send_message(chat_id, "Day traders open and close trades within the same day.", trading_menu)

    elif text == "Swing Trading":
        send_message(chat_id, "Swing trading holds trades for several days or weeks.", trading_menu)

    elif text == "Trend Trading":
        send_message(chat_id, "Trend traders follow the overall market direction.", trading_menu)

    elif text == "Risk per trade":
        send_message(chat_id, "Professional traders risk only 1% to 2% of their capital per trade.", risk_menu)

    elif text == "Stop loss":
        send_message(chat_id, "A stop loss automatically closes a trade to limit losses.", risk_menu)

    elif text == "Position sizing":
        send_message(chat_id, "Position sizing determines how much capital you risk per trade.", risk_menu)

    elif text == "Bull Market":
        send_message(chat_id, "A bull market is when prices rise for a long period.", market_menu)

    elif text == "Bear Market":
        send_message(chat_id, "A bear market is when prices fall for a long period.", market_menu)

    elif text == "Market Sentiment":
        send_message(chat_id, "Market sentiment reflects the overall mood of investors.", market_menu)

    elif text == "BTC Price":
        send_message(chat_id, get_crypto_prices(), price_menu)

    elif text == "ETH Price":
        send_message(chat_id, get_crypto_prices(), price_menu)

    elif text == "SOL Price":
        send_message(chat_id, get_crypto_prices(), price_menu)

    elif text == "📈 BTC Chart":
        chart_url = "https://quickchart.io/chart?c={type:'line',data:{labels:['1','2','3','4','5'],datasets:[{label:'BTC',data:[42000,43000,41000,45000,47000]}]}}"
        send_photo(chat_id, chart_url, "Bitcoin chart example", price_menu)

    elif text == "AI Market Analysis":
        send_message(chat_id, "AI analyzes trend strength, volatility and market sentiment to estimate market direction.", ai_menu)

    elif text == "Trend Strength":
        send_message(chat_id, "Trend strength measures how powerful the market movement is.", ai_menu)

    elif text == "Volatility":
        send_message(chat_id, "Volatility measures how much the price moves in a short time.", ai_menu)

    elif text == "What are Altcoins":
        send_message(chat_id, "Altcoins are all cryptocurrencies other than Bitcoin.", altcoin_menu)

    elif text == "Popular Altcoins":
        send_message(chat_id, "Popular altcoins include Ethereum, Solana, Cardano and Avalanche.", altcoin_menu)

    elif text == "What is Staking":
        send_message(chat_id, "Staking allows you to earn rewards by locking crypto to support a blockchain.", staking_menu)

    elif text == "Staking Rewards":
        send_message(chat_id, "Staking rewards are earnings received for helping secure the network.", staking_menu)

    elif text == "Portfolio Diversification":
        send_message(chat_id, "Diversification reduces risk by investing in different assets.", portfolio_menu)

    elif text == "Long term strategy":
        send_message(chat_id, "Long term investors hold assets for years to capture growth.", portfolio_menu)

    elif text == "Latest Crypto News":
        send_message(chat_id, get_crypto_news(), news_menu)

    elif text == "⬅ Back":
        send_message(chat_id, "Main menu", main_menu)

    else:
        send_message(chat_id, "Choose a valid option", main_menu)

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
)
