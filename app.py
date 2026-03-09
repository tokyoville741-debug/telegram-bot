import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}"

user_state = {}

main_menu = [
["📚 Learn","📈 Trading"],
["⚠️ Risk","📊 Market"],
["💰 Price","🧠 AI Analysis"],
["🌕 Altcoins","🔒 Staking"],
["💼 Portfolio","📰 News"]
]

def send_message(chat_id,text,keyboard=None):

    data = {
    "chat_id":chat_id,
    "text":text,
    "parse_mode":"Markdown"
    }

    if keyboard:
        data["reply_markup"]={
        "keyboard":keyboard,
        "resize_keyboard":True
        }

    requests.post(f"{TELEGRAM_URL}/sendMessage",json=data)


@app.route("/")
def home():
    return "Bot running"


@app.route("/webhook",methods=["POST"])
def webhook():

    data=request.json

    if "message" not in data:
        return "ok"

    chat_id=data["message"]["chat"]["id"]
    text=data["message"].get("text","")

    state=user_state.get(chat_id,"main")


# START

    if text in ["/start","menu","Menu"]:

        user_state[chat_id]="main"

        reply="""
🤖 OpenClaw AI Coach

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

        send_message(chat_id,reply,main_menu)


# LEARN MENU

    elif text in ["1","📚 Learn"] and state=="main":

        user_state[chat_id]="learn"

        reply="""
📚 Crypto Learning Hub

1️⃣ What is Blockchain
2️⃣ What is Bitcoin
3️⃣ What is Crypto Trading
4️⃣ Spot vs Futures
5️⃣ Risk Management
"""

        send_message(chat_id,reply,[["🔙 Back"]])


# LEARN CONTENT

    elif text=="1" and state=="learn":

        reply="""
🔗 Blockchain

Blockchain is a decentralized ledger
that records transactions across many computers.

Features
• transparency
• security
• decentralization
"""

        send_message(chat_id,reply,[["🔙 Back"]])


    elif text=="2" and state=="learn":

        reply="""
₿ Bitcoin

Bitcoin is the first cryptocurrency
created in 2009 by Satoshi Nakamoto.

Purpose
• decentralized payments
• peer to peer money
"""

        send_message(chat_id,reply,[["🔙 Back"]])


# TRADING MENU

    elif text in ["2","📈 Trading"] and state=="main":

        user_state[chat_id]="trading"

        reply="""
📈 Trading Basics

1️⃣ Support & Resistance
2️⃣ Market Trends
3️⃣ Moving Averages
4️⃣ RSI Indicator
5️⃣ Market Cycles
"""

        send_message(chat_id,reply,[["🔙 Back"]])


# TRADING CONTENT

    elif text=="1" and state=="trading":

        reply="""
📊 Support & Resistance

Support = price where buyers enter

Resistance = price where sellers appear

Used for trade entries and exits.
"""

        send_message(chat_id,reply,[["🔙 Back"]])


# RISK MENU

    elif text in ["3","⚠️ Risk"] and state=="main":

        user_state[chat_id]="risk"

        reply="""
⚠️ Risk Management

1️⃣ Position Size
2️⃣ Stop Loss
3️⃣ Diversification
4️⃣ Emotional Control
5️⃣ Risk Reward
"""

        send_message(chat_id,reply,[["🔙 Back"]])


# MARKET MENU

    elif text in ["4","📊 Market"] and state=="main":

        user_state[chat_id]="market"

        reply="""
📊 Market Concepts

1️⃣ Bull Market
2️⃣ Bear Market
3️⃣ Liquidity
4️⃣ Volatility
5️⃣ Market Cycles
"""

        send_message(chat_id,reply,[["🔙 Back"]])


# PRICE

    elif text in ["5","💰 Price"]:

        url="https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd"

        r=requests.get(url).json()

        btc=r["bitcoin"]["usd"]
        eth=r["ethereum"]["usd"]
        sol=r["solana"]["usd"]

        reply=f"""
💰 Live Crypto Prices

BTC : ${btc}
ETH : ${eth}
SOL : ${sol}
"""

        send_message(chat_id,reply,[["🔙 Back"]])


# BACK BUTTON

    elif text=="🔙 Back":

        user_state[chat_id]="main"

        send_message(chat_id,"Main Menu",main_menu)


# DEFAULT

    else:

        reply="""
🧠 Ask me about crypto

Examples
• What is Bitcoin
• How to trade
• Crypto market
"""

        send_message(chat_id,reply,main_menu)


    return "ok"


if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
