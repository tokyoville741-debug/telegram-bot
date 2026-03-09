import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ---------------- SEND FUNCTION ----------------

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

price_menu = [
    ["BTC Price", "ETH Price"],
    ["SOL Price", "Top 5 Prices"],
    ["⬅ Back"]
]

news_menu = [
    ["Latest News"],
    ["⬅ Back"]
]

# ---------------- API ----------------

def get_price(coin):

    try:

        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": coin, "vs_currencies": "usd"}

        r = requests.get(url, params=params)
        data = r.json()

        return data[coin]["usd"]

    except:
        return "Unavailable"


def get_top_prices():

    try:

        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {"vs_currency":"usd","order":"market_cap_desc","per_page":5,"page":1}

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


# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return "Bot running"


@app.route("/webhook", methods=["POST"])
def webhook():

    try:

        data = request.get_json()

        if not data:
            return jsonify({"ok":True})

        message = data.get("message")

        if not message:
            return jsonify({"ok":True})

        chat_id = message["chat"]["id"]
        text = message.get("text","")

        text = text.lower()

# ---------------- START ----------------

        if "/start" in text:

            msg = """
🤖 <b>OpenClaw AI Coach</b>

Welcome to your crypto learning assistant.

This bot helps you understand:

📚 Cryptocurrency fundamentals  
📈 Trading strategies  
⚠ Risk management  
📊 Market analysis  
💰 Live crypto prices  
🌕 Altcoins insights  
🔒 Staking systems  
💼 Portfolio building  
📰 Latest crypto news
"""

            send_message(chat_id,msg,main_menu)

# ---------------- LEARN ----------------

        elif "learn" in text:
            send_message(chat_id,"📚 Crypto Education",learn_menu)

        elif "blockchain" in text:

            msg = """
🔗 <b>What is Blockchain?</b>

Blockchain is a decentralized digital ledger that records transactions across a distributed network of computers.

Instead of storing information in one central database, blockchain stores data in blocks that are linked together chronologically. Each block contains:

• Transaction data  
• A timestamp  
• A cryptographic hash of the previous block  

This structure makes the system extremely secure because altering one block would require changing all subsequent blocks across the entire network.

Blockchain operates through consensus mechanisms such as Proof of Work or Proof of Stake, which ensure that all participants agree on the validity of transactions.

Because of this design, blockchain provides:

• Transparency  
• Security  
• Decentralization  
• Resistance to censorship  

It is the core technology behind cryptocurrencies like Bitcoin and many other decentralized applications.
"""

            send_message(chat_id,msg,learn_menu)

        elif "bitcoin basics" in text:

            msg = """
₿ <b>Bitcoin Basics</b>

Bitcoin is the first decentralized cryptocurrency, created in 2009 by an anonymous person or group known as Satoshi Nakamoto.

Key characteristics of Bitcoin include:

• A fixed maximum supply of 21 million coins  
• A decentralized network with no central authority  
• Transactions verified by miners using Proof of Work  
• Transparent and immutable transaction records stored on the blockchain  

Bitcoin can be used for:

• Digital payments  
• International transfers  
• Long-term investment (store of value)  

Many investors consider Bitcoin to be "digital gold" because of its scarcity and resistance to inflation.
"""

            send_message(chat_id,msg,learn_menu)

# ---------------- TRADING ----------------

        elif "trading" in text:
            send_message(chat_id,"📈 Trading Strategies",trading_menu)

        elif "day trading" in text:

            msg = """
📈 <b>Day Trading</b>

Day trading is a strategy where traders open and close positions within the same day.

The goal is to profit from small price movements during short periods of time.

Day traders typically rely on:

• Technical analysis  
• Chart patterns  
• Indicators such as RSI and MACD  
• High market liquidity  

Because the crypto market operates 24/7, day traders must monitor the market frequently and apply strict risk management.

This strategy is considered high risk but can produce frequent opportunities.
"""

            send_message(chat_id,msg,trading_menu)

# ---------------- PRICE ----------------

        elif "btc price" in text:
            send_message(chat_id,f"BTC Price = ${get_price('bitcoin')}",price_menu)

        elif "eth price" in text:
            send_message(chat_id,f"ETH Price = ${get_price('ethereum')}",price_menu)

        elif "sol price" in text:
            send_message(chat_id,f"SOL Price = ${get_price('solana')}",price_menu)

        elif "top 5 prices" in text:
            send_message(chat_id,get_top_prices(),price_menu)

# ---------------- NEWS ----------------

        elif "news" in text:
            send_message(chat_id,get_news(),news_menu)

# ---------------- BACK ----------------

        elif "back" in text:
            send_message(chat_id,"Main Menu",main_menu)

        else:

            send_message(chat_id,
            "🤖 Ask me anything about cryptocurrency, trading or blockchain technology.",
            main_menu)

    except Exception as e:
        print("ERROR:",e)

    return jsonify({"ok":True})


if __name__ == "__main__":

    port = int(os.environ.get("PORT",10000))

    app.run(host="0.0.0.0",port=port)
