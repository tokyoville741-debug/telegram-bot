import requests
import time
import os
import threading
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN")
LLAMA_API_KEY = os.environ.get("LLAMA_API_KEY")

URL = f"https://api.telegram.org/bot{TOKEN}/"
LLAMA_URL = "https://api.llama-api.com/chat/completions"

app = Flask(__name__)

@app.route("/")
def home():
    return "Crypto AI Bot running 🚀"


# =========================
# MAIN MENU
# =========================

main_menu = {
"keyboard":[
["1️⃣ 📚 Learn","2️⃣ 📈 Trading"],
["3️⃣ ⚠ Risk","4️⃣ 📊 Market"],
["5️⃣ 💰 Price","6️⃣ 📊 Charts"],
["7️⃣ 🌕 Altcoins","8️⃣ 🔒 Staking"],
["9️⃣ 💼 Portfolio","🔟 📰 News"],
["🧠 AI Assistant"]
],
"resize_keyboard":True
}


# =========================
# PRICE MENU
# =========================

price_menu = {
"keyboard":[
["BTC","ETH"],
["SOL","BNB"],
["⬅ Back"]
],
"resize_keyboard":True
}


# =========================
# CHART MENU (UNCHANGED)
# =========================

chart_menu = {
"keyboard":[
["BTC Chart","ETH Chart"],
["SOL Chart","BNB Chart"],
["⬅ Back"]
],
"resize_keyboard":True
}


# =========================
# BACK MENU
# =========================

back_menu = {
"keyboard":[["⬅ Back"]],
"resize_keyboard":True
}


# =========================
# SEND MESSAGE
# =========================

def send(chat_id,text,keyboard=None):

    payload={
    "chat_id":chat_id,
    "text":text
    }

    if keyboard:
        payload["reply_markup"]=keyboard

    try:
        requests.post(URL+"sendMessage",json=payload,timeout=10)
    except Exception as e:
        print("Send error:",e)


# =========================
# PRICE API
# =========================

def price(coin):

    try:

        r=requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={"ids":coin,"vs_currencies":"usd"},
        timeout=10
        )

        data=r.json()

        if coin in data:
            return data[coin]["usd"]

        return "Unavailable"

    except:
        return "Unavailable"


# =========================
# NEWS (UNCHANGED)
# =========================

def crypto_news():

    try:

        r=requests.get(
        "https://min-api.cryptocompare.com/data/v2/news/?lang=EN",
        timeout=10
        )

        news=r.json().get("Data",[])[:5]

        text="📰 Latest Crypto News\n\n"

        for n in news:
            text+=f"{n['title']}\n{n['url']}\n\n"

        return text

    except:
        return "News unavailable."


# =========================
# AI
# =========================

def llama_ai(question):

    if not LLAMA_API_KEY:
        return "AI unavailable."

    headers={
    "Authorization":f"Bearer {LLAMA_API_KEY}",
    "Content-Type":"application/json"
    }

    data={
    "model":"meta-llama-3.3-70b-instruct",
    "messages":[
    {"role":"system","content":"You are a professional crypto assistant."},
    {"role":"user","content":question}
    ]
    }

    try:

        r=requests.post(
        LLAMA_URL,
        headers=headers,
        json=data,
        timeout=30
        )

        result=r.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"]

        return "AI unavailable."

    except:
        return "AI unavailable."


# =========================
# TELEGRAM UPDATES
# =========================

def get_updates(offset):

    try:

        r=requests.get(
        URL+"getUpdates",
        params={"offset":offset,"timeout":25},
        timeout=30
        )

        return r.json()

    except:
        return {}


# =========================
# BOT LOOP
# =========================

def run_bot():

    offset=None
    ai_mode={}

    while True:

        data=get_updates(offset)

        if not data or "result" not in data:
            time.sleep(2)
            continue

        for update in data["result"]:

            offset=update["update_id"]+1

            if "message" not in update:
                continue

            msg=update["message"]

            if "text" not in msg:
                continue

            chat=msg["chat"]["id"]
            text=msg["text"].strip()


            # =====================
            # START
            # =====================

            if text=="/start":

                welcome="""
🤖 Welcome to the Crypto AI Assistant

This bot helps you learn cryptocurrency step by step.

Menu guide:

1️⃣ Learn → Understand crypto basics
2️⃣ Trading → Learn how trading works
3️⃣ Risk → Risk management rules
4️⃣ Market → Market cycle explanation
5️⃣ Price → Live crypto prices
6️⃣ Charts → TradingView charts
7️⃣ Altcoins → What altcoins are
8️⃣ Staking → Earn rewards with crypto
9️⃣ Portfolio → Example crypto portfolio
🔟 News → Latest crypto news
🧠 AI Assistant → Ask any crypto question
"""

                send(chat,welcome,main_menu)


            # =====================
            # LEARN
            # =====================

            elif text=="1️⃣ 📚 Learn":

                send(chat,
"""
📚 WHAT IS CRYPTOCURRENCY?

Cryptocurrency is a digital form of money that exists on the internet.

Unlike traditional money controlled by banks, cryptocurrencies are powered by a technology called blockchain.

Blockchain is a decentralized ledger that records every transaction securely.

Key advantages:

• No central authority  
• Transparent transactions  
• Global accessibility  
• High security through cryptography
""",
                back_menu)


            # =====================
            # TRADING
            # =====================

            elif text=="2️⃣ 📈 Trading":

                send(chat,
"""
📈 WHAT IS CRYPTO TRADING?

Crypto trading is the act of buying and selling cryptocurrencies in order to make a profit.

Traders analyze price movements using charts and market data.

Common trading styles include:

• Day trading
• Swing trading
• Long-term investing

Successful trading requires discipline, strategy, and risk management.
""",
                back_menu)


            # =====================
            # RISK
            # =====================

            elif text=="3️⃣ ⚠ Risk":

                send(chat,
"""
⚠ RISK MANAGEMENT

Risk management is the most important rule in trading.

Golden rules:

• Never risk more than 2% of your capital on one trade.
• Always use stop-loss orders.
• Never trade emotionally.
• Diversify your investments.

Protecting your capital is more important than chasing profits.
""",
                back_menu)


            # =====================
            # MARKET
            # =====================

            elif text=="4️⃣ 📊 Market":

                send(chat,
"""
📊 CRYPTO MARKET CYCLES

Markets move in cycles:

1️⃣ Accumulation  
Smart investors slowly buy.

2️⃣ Uptrend  
Prices start rising quickly.

3️⃣ Distribution  
Early investors begin selling.

4️⃣ Downtrend  
Prices fall and market resets.

Understanding cycles helps traders avoid buying at the top.
""",
                back_menu)


            # =====================
            # PRICE MENU
            # =====================

            elif text=="5️⃣ 💰 Price":

                send(chat,"Choose a coin:",price_menu)


            elif text=="BTC":
                send(chat,f"₿ Bitcoin price: ${price('bitcoin')}")

            elif text=="ETH":
                send(chat,f"Ξ Ethereum price: ${price('ethereum')}")

            elif text=="SOL":
                send(chat,f"◎ Solana price: ${price('solana')}")

            elif text=="BNB":
                send(chat,f"BNB price: ${price('binancecoin')}")


            # =====================
            # CHARTS (UNCHANGED)
            # =====================

            elif text=="6️⃣ 📊 Charts":
                send(chat,"Choose chart:",chart_menu)

            elif text=="BTC Chart":
                send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT")

            elif text=="ETH Chart":
                send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:ETHUSDT")

            elif text=="SOL Chart":
                send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:SOLUSDT")

            elif text=="BNB Chart":
                send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:BNBUSDT")


            # =====================
            # ALTCOINS
            # =====================

            elif text=="7️⃣ 🌕 Altcoins":

                send(chat,
"""
🌕 WHAT ARE ALTCOINS?

Altcoins are all cryptocurrencies other than Bitcoin.

Examples include:

• Ethereum
• Solana
• Cardano
• Avalanche

Many altcoins focus on new technologies like smart contracts, decentralized finance (DeFi), and Web3 applications.
""",
                back_menu)


            # =====================
            # STAKING
            # =====================

            elif text=="8️⃣ 🔒 Staking":

                send(chat,
"""
🔒 WHAT IS STAKING?

Staking allows crypto holders to earn rewards by locking their coins to support a blockchain network.

Benefits:

• Passive income
• Network security
• Long-term investment strategy

Many blockchains like Ethereum and Solana support staking.
""",
                back_menu)


            # =====================
            # PORTFOLIO
            # =====================

            elif text=="9️⃣ 💼 Portfolio":

                send(chat,
"""
💼 EXAMPLE CRYPTO PORTFOLIO

A balanced portfolio could look like:

50% Bitcoin  
25% Ethereum  
15% Altcoins  
10% Stablecoins

Diversification helps reduce investment risk.
""",
                back_menu)


            # =====================
            # NEWS (UNCHANGED)
            # =====================

            elif text=="🔟 📰 News":
                send(chat,crypto_news(),back_menu)


            # =====================
            # AI MODE
            # =====================

            elif text=="🧠 AI Assistant":

                ai_mode[chat]=True
                send(chat,"Ask any crypto question.",back_menu)


            elif text=="⬅ Back":

                ai_mode[chat]=False
                send(chat,"Main menu",main_menu)


            else:

                if ai_mode.get(chat):
                    reply=llama_ai(text)
                    send(chat,reply)
                else:
                    send(chat,"Choose an option.",main_menu)

        time.sleep(1)


# =========================
# START BOT
# =========================

if __name__=="__main__":

    bot_thread=threading.Thread(target=run_bot)
    bot_thread.start()

    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
