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

main_menu = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    ["10"]
]

learn_menu = [
    ["1 What is Blockchain"],
    ["2 Bitcoin Basics"],
    ["3 Trading Psychology"],
    ["4 Market Cycles"],
    ["⬅ Back"]
]

trading_menu = [
    ["1 Scalping"],
    ["2 Day Trading"],
    ["3 Swing Trading"],
    ["4 Trend Trading"],
    ["⬅ Back"]
]

risk_menu = [
    ["1 Risk per trade"],
    ["2 Stop loss"],
    ["3 Position sizing"],
    ["⬅ Back"]
]

market_menu = [
    ["1 Bull Market"],
    ["2 Bear Market"],
    ["3 Market Sentiment"],
    ["⬅ Back"]
]

price_menu = [
    ["1 BTC"],
    ["2 ETH"],
    ["3 SOL"],
    ["⬅ Back"]
]

ai_menu = [
    ["1 Trend strength"],
    ["2 Volatility"],
    ["3 Market sentiment"],
    ["⬅ Back"]
]

altcoin_menu = [
    ["1 What are Altcoins"],
    ["2 Popular Altcoins"],
    ["⬅ Back"]
]

staking_menu = [
    ["1 What is Staking"],
    ["2 Staking Rewards"],
    ["⬅ Back"]
]

portfolio_menu = [
    ["1 Portfolio Diversification"],
    ["2 Long term strategy"],
    ["⬅ Back"]
]

news_menu = [
    ["1 Latest Crypto News"],
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
BTC : ${btc}
ETH : ${eth}
SOL : ${sol}
"""

    except Exception as e:
        print("Price API error:", e)
        return "⚠ Unable to fetch prices."

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

    state = user_state.get(chat_id, "main")

    if not text:
        return jsonify({"status": "ok"}), 200

    if text in ["/start", "menu", "Menu"]:

        user_state[chat_id] = "main"

        reply = """
Welcome to the Crypto Learning Bot

Choose a section
"""

        send_message(chat_id, reply, main_menu)

    elif text == "1":
        user_state[chat_id] = "learn"
        send_message(chat_id, "Learn section", learn_menu)

    elif text == "2":
        user_state[chat_id] = "trading"
        send_message(chat_id, "Trading section", trading_menu)

    elif text == "3":
        user_state[chat_id] = "risk"
        send_message(chat_id, "Risk management section", risk_menu)

    elif text == "4":
        user_state[chat_id] = "market"
        send_message(chat_id, "Market section", market_menu)

    elif text == "5":
        user_state[chat_id] = "price"
        send_message(chat_id, "Crypto prices", price_menu)

    elif text == "6":
        user_state[chat_id] = "ai"
        send_message(chat_id, "AI analysis", ai_menu)

    elif text == "7":
        user_state[chat_id] = "altcoins"
        send_message(chat_id, "Altcoins section", altcoin_menu)

    elif text == "8":
        user_state[chat_id] = "staking"
        send_message(chat_id, "Staking section", staking_menu)

    elif text == "9":
        user_state[chat_id] = "portfolio"
        send_message(chat_id, "Portfolio section", portfolio_menu)

    elif text == "10":
        user_state[chat_id] = "news"
        send_message(chat_id, "News section", news_menu)

    elif text == "1 What is Blockchain":
        send_message(chat_id, "Blockchain is a decentralized digital ledger that records transactions across many computers. It is secure, transparent and cannot be easily changed.", learn_menu)

    elif text == "2 Bitcoin Basics":
        send_message(chat_id, "Bitcoin is the first cryptocurrency created in 2009 by Satoshi Nakamoto. It allows peer to peer payments without banks.", learn_menu)

    elif text == "3 Trading Psychology":
        send_message(chat_id, "Trading psychology refers to the emotions and mindset that influence trading decisions such as fear, greed and discipline.", learn_menu)

    elif text == "4 Market Cycles":
        send_message(chat_id, "Markets move in cycles: accumulation, uptrend, distribution and downtrend.", learn_menu)

    elif text == "1 Scalping":
        send_message(chat_id, "Scalping is a fast trading strategy where traders take small profits from many trades.", trading_menu)

    elif text == "2 Day Trading":
        send_message(chat_id, "Day trading means opening and closing trades within the same day.", trading_menu)

    elif text == "3 Swing Trading":
        send_message(chat_id, "Swing trading involves holding trades for several days or weeks.", trading_menu)

    elif text == "4 Trend Trading":
        send_message(chat_id, "Trend trading means following the overall market direction.", trading_menu)

    elif text == "1 Risk per trade":
        send_message(chat_id, "Professional traders usually risk only 1% to 2% of their capital per trade.", risk_menu)

    elif text == "2 Stop loss":
        send_message(chat_id, "A stop loss automatically closes your trade to limit losses.", risk_menu)

    elif text == "3 Position sizing":
        send_message(chat_id, "Position sizing helps control how much money you risk in each trade.", risk_menu)

    elif text == "1 Bull Market":
        send_message(chat_id, "A bull market is when prices rise for a long period.", market_menu)

    elif text == "2 Bear Market":
        send_message(chat_id, "A bear market is when prices fall for a long period.", market_menu)

    elif text == "3 Market Sentiment":
        send_message(chat_id, "Market sentiment represents the overall attitude of investors.", market_menu)

    elif text == "1 BTC":
        prices = get_crypto_prices()
        send_message(chat_id, prices, price_menu)

    elif text == "2 ETH":
        prices = get_crypto_prices()
        send_message(chat_id, prices, price_menu)

    elif text == "3 SOL":
        prices = get_crypto_prices()
        send_message(chat_id, prices, price_menu)

    elif text == "1 Trend strength":
        send_message(chat_id, "AI analyzes whether the trend is strong or weak based on data.", ai_menu)

    elif text == "2 Volatility":
        send_message(chat_id, "Volatility measures how much the price moves in a short time.", ai_menu)

    elif text == "3 Market sentiment":
        send_message(chat_id, "AI can analyze news and social media to estimate market sentiment.", ai_menu)

    elif text == "1 What are Altcoins":
        send_message(chat_id, "Altcoins are all cryptocurrencies other than Bitcoin.", altcoin_menu)

    elif text == "2 Popular Altcoins":
        send_message(chat_id, "Popular altcoins include Ethereum, Solana, Cardano and Avalanche.", altcoin_menu)

    elif text == "1 What is Staking":
        send_message(chat_id, "Staking allows you to earn rewards by locking crypto to support a blockchain network.", staking_menu)

    elif text == "2 Staking Rewards":
        send_message(chat_id, "Staking rewards are paid to users who help secure the network.", staking_menu)

    elif text == "1 Portfolio Diversification":
        send_message(chat_id, "Diversification means investing in different assets to reduce risk.", portfolio_menu)

    elif text == "2 Long term strategy":
        send_message(chat_id, "Long term investing focuses on holding assets for years.", portfolio_menu)

    elif text == "1 Latest Crypto News":
        send_message(chat_id, "Follow reliable sources like CoinDesk or CoinTelegraph for crypto news.", news_menu)

    elif text == "⬅ Back":
        user_state[chat_id] = "main"
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
