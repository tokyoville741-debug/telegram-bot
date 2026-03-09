import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}"

user_state = {}

main_menu = [
    ["📚 Learn", "📈 Trading"],
    ["⚠️ Risk", "📊 Market"],
    ["💰 Price", "🧠 AI Analysis"],
    ["🌕 Altcoins", "🔒 Staking"],
    ["💼 Portfolio", "📰 News"]
]

def send_message(chat_id, text, keyboard=None):

    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }

    if keyboard:
        data["reply_markup"] = {
            "keyboard": keyboard,
            "resize_keyboard": True
        }

    requests.post(f"{TELEGRAM_URL}/sendMessage", json=data)


@app.route("/")
def home():
    return "OpenClaw AI Coach is running 🚀"


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    if "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text","")

    if chat_id not in user_state:
        user_state[chat_id] = "main"


# START MENU

    if text in ["/start","Menu","menu"]:

        user_state[chat_id] = "main"

        reply = """
🤖 *OpenClaw AI Coach*

1️⃣ Learn  
2️⃣ Trading  
3️⃣ Risk  
4️⃣ Market  
5️⃣ Price  
6️⃣ AI Analysis  
7️⃣ Altcoins  
8️⃣ Staking  
9️⃣ Portfolio  
🔟 News
"""

        send_message(chat_id, reply, main_menu)


# LEARN MENU

    elif text in ["1","📚 Learn"] and user_state[chat_id] == "main":

        user_state[chat_id] = "learn"

        reply = """
📚 *Crypto Learning Hub*

1️⃣ What is Blockchain  
2️⃣ What is Bitcoin  
3️⃣ What is Crypto Trading  
4️⃣ Spot vs Futures  
5️⃣ Risk Management
"""

        send_message(chat_id, reply, [["🔙 Back"]])


# LEARN EXPLANATIONS

    elif text == "1" and user_state[chat_id] == "learn":

        reply = """
🔗 *Blockchain*

A decentralized digital ledger that records
transactions across multiple computers.

Key features
• transparency  
• security  
• decentralization
"""

        send_message(chat_id, reply, [["🔙 Back"]])


    elif text == "2" and user_state[chat_id] == "learn":

        reply = """
₿ *Bitcoin*

The first cryptocurrency created in 2009
by Satoshi Nakamoto.

Purpose
• peer to peer money  
• decentralized payments
"""

        send_message(chat_id, reply, [["🔙 Back"]])


# TRADING MENU

    elif text in ["2","📈 Trading"] and user_state[chat_id] == "main":

        user_state[chat_id] = "trading"

        reply = """
📈 *Trading Basics*

1️⃣ Support & Resistance  
2️⃣ Market Trends  
3️⃣ Moving Averages  
4️⃣ RSI Indicator  
5️⃣ Market Cycles
"""

        send_message(chat_id, reply, [["🔙 Back"]])


# TRADING EXPLANATION

    elif text == "1" and user_state[chat_id] == "trading":

        reply = """
📊 *Support & Resistance*

Support = price level where buyers appear.

Resistance = price level where sellers appear.

Traders use these zones to plan
entries and exits.
"""

        send_message(chat_id, reply, [["🔙 Back"]])


# RISK MENU

    elif text in ["3","⚠️ Risk"] and user_state[chat_id] == "main":

        user_state[chat_id] = "risk"

        reply = """
⚠️ *Risk Management*

1️⃣ Position Sizing  
2️⃣ Stop Loss  
3️⃣ Diversification  
4️⃣ Emotional Control  
5️⃣ Risk Reward
"""

        send_message(chat_id, reply, [["🔙 Back"]])


# MARKET MENU

    elif text in ["4","📊 Market"] and user_state[chat_id] == "main":

        user_state[chat_id] = "market"

        reply = """
📊 *Market Analysis*

1️⃣ Bull Market  
2️⃣ Bear Market  
3️⃣ Market Liquidity  
4️⃣ Market Volatility  
5️⃣ Market Cycles
"""

        send_message(chat_id, reply, [["🔙 Back"]])


# PRICE

    elif text in ["5","💰 Price"]:

        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd"

        r = requests.get(url).json()

        btc = r["bitcoin"]["usd"]
        eth = r["ethereum"]["usd"]
        sol = r["solana"]["usd"]

        reply = f"""
💰 *Live Crypto Prices*

BTC : ${btc}  
ETH : ${eth}  
SOL : ${sol}
"""

        send_message(chat_id, reply, [["🔙 Back"]])


# BACK BUTTON

    elif text == "🔙 Back":

        user_state[chat_id] = "main"

        send_message(chat_id, "Main Menu", main_menu)


# DEFAULT AI MESSAGE

    else:

        reply = """
🧠 Ask me anything about crypto.

Example
• What is Bitcoin
• How to trade
• Crypto market analysis
"""

        send_message(chat_id, reply, main_menu)


    return "ok"


if __name__ == "__main__":
    app.run()
