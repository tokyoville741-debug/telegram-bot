import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

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

    api = f"{TELEGRAM_API}/sendPhoto"

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

    requests.post(api, json=payload)

# MENUS

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

price_menu = [
    ["BTC Price", "📈 BTC Chart"],
    ["ETH Price", "📈 ETH Chart"],
    ["SOL Price", "📈 SOL Chart"],
    ["⬅ Back"]
]

# PRICE FUNCTIONS

def get_price(coin):

    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": coin,
        "vs_currencies": "usd"
    }

    r = requests.get(url, params=params)
    data = r.json()

    return data[coin]["usd"]

# NEWS

def get_news():

    url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"

    r = requests.get(url)

    data = r.json()

    text = "📰 Latest Crypto News\n\n"

    for n in data["Data"][:5]:

        text += f"{n['title']}\n{n['url']}\n\n"

    return text

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

    # START

    if text == "/start":

        reply = """
🤖 <b>OpenClaw AI Coach</b>

Welcome to the Crypto Learning Bot.

Learn cryptocurrency, trading strategies and market analysis directly inside Telegram.

📚 Crypto Education
📈 Trading Strategies
⚠ Risk Management
📊 Market Knowledge
💰 Live Prices
🧠 AI Market Insights
🌕 Altcoins
🔒 Staking
💼 Portfolio Strategy
📰 Crypto News

<i>Powered by Python & Telegram Bot API</i>
"""

        send_message(chat_id, reply, main_menu)

    # MENUS

    elif text == "📚 Learn":
        send_message(chat_id, "📚 Crypto Education", learn_menu)

    elif text == "💰 Price":
        send_message(chat_id, "💰 Crypto Prices", price_menu)

    elif text == "📰 News":
        send_message(chat_id, get_news(), main_menu)

    # DEFINITIONS

    elif text == "What is Blockchain":

        msg = """
🔗 Blockchain

Blockchain is a decentralized digital ledger that records transactions across a distributed network of computers.

Instead of relying on a central authority, the system uses consensus between many nodes.

Key features:

• Decentralization  
• Transparency  
• Security through cryptography  
• Immutability of records

Blockchain technology is the foundation of cryptocurrencies like Bitcoin and Ethereum.
"""

        send_message(chat_id, msg, learn_menu)

    elif text == "Bitcoin Basics":

        msg = """
₿ Bitcoin Basics

Bitcoin is the first decentralized cryptocurrency created in 2009 by Satoshi Nakamoto.

It allows users to send digital money directly to each other without banks or intermediaries.

Main characteristics:

• Limited supply (21 million BTC)
• Decentralized network
• Peer-to-peer transactions
• Secured by mining

Bitcoin is often referred to as "digital gold".
"""

        send_message(chat_id, msg, learn_menu)

    # PRICES

    elif text == "BTC Price":

        price = get_price("bitcoin")

        send_message(chat_id, f"💰 BTC Price\n\nBitcoin = ${price}", price_menu)

    elif text == "ETH Price":

        price = get_price("ethereum")

        send_message(chat_id, f"💰 ETH Price\n\nEthereum = ${price}", price_menu)

    elif text == "SOL Price":

        price = get_price("solana")

        send_message(chat_id, f"💰 SOL Price\n\nSolana = ${price}", price_menu)

    # CHARTS

    elif text == "📈 BTC Chart":

        url = "https://quickchart.io/chart?c={type:'line',data:{labels:['1','2','3','4','5'],datasets:[{label:'BTC',data:[62000,63000,64000,65000,66000]}]}}"

        send_photo(chat_id, url, "📈 Bitcoin Chart", price_menu)

    elif text == "📈 ETH Chart":

        url = "https://quickchart.io/chart?c={type:'line',data:{labels:['1','2','3','4','5'],datasets:[{label:'ETH',data:[3000,3100,3200,3300,3400]}]}}"

        send_photo(chat_id, url, "📈 Ethereum Chart", price_menu)

    elif text == "📈 SOL Chart":

        url = "https://quickchart.io/chart?c={type:'line',data:{labels:['1','2','3','4','5'],datasets:[{label:'SOL',data:[100,105,110,120,125]}]}}"

        send_photo(chat_id, url, "📈 Solana Chart", price_menu)

    elif text == "⬅ Back":

        send_message(chat_id, "Main Menu", main_menu)

    else:

        send_message(chat_id, "Choose a valid option", main_menu)

    return jsonify({"ok": True})

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
)
