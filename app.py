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

# ---------------- MENUS ----------------

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

# ---------------- PRICE FUNCTION ----------------

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

# ---------------- NEWS ----------------

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

        return "News unavailable right now."

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

        reply = """
🤖 <b>OpenClaw AI Coach</b>

Welcome to the Crypto Learning Bot.

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

# ---------------- MENUS ----------------

    elif text == "📚 Learn":
        send_message(chat_id, "📚 Crypto Education", learn_menu)

    elif text == "💰 Price":
        send_message(chat_id, "💰 Crypto Prices", price_menu)

    elif text == "📰 News":
        send_message(chat_id, get_news(), main_menu)

# ---------------- LEARN ----------------

    elif text == "What is Blockchain":

        msg = """
🔗 <b>Blockchain</b>

A decentralized digital ledger that records transactions across many computers.

Key features:

• Decentralization  
• Transparency  
• Cryptographic security  
• Immutable records
"""

        send_message(chat_id, msg, learn_menu)


    elif text == "Bitcoin Basics":

        msg = """
₿ <b>Bitcoin Basics</b>

Bitcoin is the first cryptocurrency created in 2009.

Key features:

• Limited supply (21M BTC)  
• Decentralized network  
• Peer-to-peer transactions  
• Secured by mining
"""

        send_message(chat_id, msg, learn_menu)


    elif text == "Trading Psychology":

        msg = """
🧠 <b>Trading Psychology</b>

Successful traders manage emotions like:

• Fear  
• Greed  
• Overconfidence  

Always follow a strategy and avoid emotional decisions.
"""

        send_message(chat_id, msg, learn_menu)


    elif text == "Market Cycles":

        msg = """
📊 <b>Market Cycles</b>

Markets move through 4 phases:

1️⃣ Accumulation  
2️⃣ Bull Market  
3️⃣ Distribution  
4️⃣ Bear Market
"""

        send_message(chat_id, msg, learn_menu)

# ---------------- TRADING ----------------

    elif text == "📈 Trading":

        msg = """
📈 <b>Crypto Trading</b>

Common strategies:

• Day Trading  
• Swing Trading  
• Long Term Holding
"""

        send_message(chat_id, msg, main_menu)

# ---------------- RISK ----------------

    elif text == "⚠ Risk":

        msg = """
⚠ <b>Risk Management</b>

Golden rules:

• Never invest more than you can lose  
• Use stop loss  
• Diversify your portfolio
"""

        send_message(chat_id, msg, main_menu)

# ---------------- MARKET ----------------

    elif text == "📊 Market":

        msg = """
📊 <b>Crypto Market</b>

Key indicators:

• Market Cap  
• BTC Dominance  
• Trading Volume
"""

        send_message(chat_id, msg, main_menu)

# ---------------- AI ANALYSIS ----------------

    elif text == "🧠 AI Analysis":

        msg = """
🧠 <b>AI Market Insight</b>

Bitcoin often drives the market.

Altcoins usually follow BTC trends.
"""

        send_message(chat_id, msg, main_menu)

# ---------------- ALTCOINS ----------------

    elif text == "🌕 Altcoins":

        msg = """
🌕 <b>Popular Altcoins</b>

• Ethereum  
• Solana  
• Cardano  
• Avalanche
"""

        send_message(chat_id, msg, main_menu)

# ---------------- STAKING ----------------

    elif text == "🔒 Staking":

        msg = """
🔒 <b>Crypto Staking</b>

Earn rewards by locking coins.

Examples:

• Ethereum  
• Solana  
• Cardano
"""

        send_message(chat_id, msg, main_menu)

# ---------------- PORTFOLIO ----------------

    elif text == "💼 Portfolio":

        msg = """
💼 <b>Portfolio Strategy</b>

Example allocation:

50% Bitcoin  
30% Ethereum  
20% Altcoins
"""

        send_message(chat_id, msg, main_menu)

# ---------------- PRICES ----------------

    elif text == "BTC Price":

        price = get_price("bitcoin")

        send_message(chat_id, f"💰 BTC Price\n\nBitcoin = ${price}", price_menu)

    elif text == "ETH Price":

        price = get_price("ethereum")

        send_message(chat_id, f"💰 ETH Price\n\nEthereum = ${price}", price_menu)

    elif text == "SOL Price":

        price = get_price("solana")

        send_message(chat_id, f"💰 SOL Price\n\nSolana = ${price}", price_menu)

# ---------------- CHARTS ----------------

    elif text == "📈 BTC Chart":

        url = "https://quickchart.io/chart?c={type:'line',data:{labels:['1','2','3','4','5'],datasets:[{label:'BTC',data:[62000,63000,64000,65000,66000]}]}}"

        send_photo(chat_id, url, "📈 Bitcoin Chart", price_menu)


    elif text == "📈 ETH Chart":

        url = "https://quickchart.io/chart?c={type:'line',data:{labels:['1','2','3','4','5'],datasets:[{label:'ETH',data:[3000,3100,3200,3300,3400]}]}}"

        send_photo(chat_id, url, "📈 Ethereum Chart", price_menu)


    elif text == "📈 SOL Chart":

        url = "https://quickchart.io/chart?c={type:'line',data:{labels:['1','2','3','4','5'],datasets:[{label:'SOL',data:[100,105,110,120,125]}]}}"

        send_photo(chat_id, url, "📈 Solana Chart", price_menu)

# ---------------- BACK ----------------

    elif text == "⬅ Back":

        send_message(chat_id, "Main Menu", main_menu)

# ---------------- DEFAULT ----------------

    else:

        send_message(chat_id, "Choose a valid option", main_menu)

    return jsonify({"ok": True})


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
        )
