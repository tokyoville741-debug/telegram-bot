import os
import requests
import time
import threading
from flask import Flask

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/"

ai_mode = {}

@app.route("/")
def home():
    return "Crypto AI Bot running"

# ===================== MENUS =====================

main_menu={
"keyboard":[
["📚 Learn","📈 Trading"],
["⚠ Risk","📊 Market"],
["💰 Price","📉 Charts"],
["🌕 Altcoins","🔒 Staking"],
["💼 Portfolio","📰 News"],
["🧠 AI Assistant"]
],
"resize_keyboard":True
}

back_menu={"keyboard":[["⬅ Back"]],"resize_keyboard":True}

learn_menu={
"keyboard":[
["What is Crypto","Blockchain"],
["Bitcoin","Wallets"],
["DeFi"],
["⬅ Back"]
],
"resize_keyboard":True
}

trading_menu={
"keyboard":[
["Spot Trading","Futures Trading"],
["Technical Analysis","Trading Strategies"],
["⬅ Back"]
],
"resize_keyboard":True
}

risk_menu={
"keyboard":[
["Stop Loss","Risk Reward"],
["Position Size"],
["⬅ Back"]
],
"resize_keyboard":True
}

market_menu={
"keyboard":[
["Bull Market","Bear Market"],
["Market Cycle"],
["⬅ Back"]
],
"resize_keyboard":True
}

price_menu={
"keyboard":[
["BTC","ETH"],
["BNB","SOL"],
["⬅ Back"]
],
"resize_keyboard":True
}

chart_menu={
"keyboard":[
["BTC Chart","ETH Chart"],
["BNB Chart","SOL Chart"],
["⬅ Back"]
],
"resize_keyboard":True
}

alt_menu={
"keyboard":[
["Ethereum","Solana"],
["Cardano"],
["⬅ Back"]
],
"resize_keyboard":True
}

staking_menu={
"keyboard":[
["What is Staking","Staking Rewards"],
["Staking Risks"],
["⬅ Back"]
],
"resize_keyboard":True
}

portfolio_menu={
"keyboard":[
["Diversification","Long Term Strategy"],
["Portfolio Example"],
["⬅ Back"]
],
"resize_keyboard":True
}

news_menu={
"keyboard":[
["Bitcoin News","Market News"],
["Regulation News"],
["⬅ Back"]
],
"resize_keyboard":True
}

# ================= SEND =================

def send(chat,text,keyboard=None):

    payload={
    "chat_id":chat,
    "text":text,
    "parse_mode":"HTML"
    }

    if keyboard:
        payload["reply_markup"]=keyboard

    try:
        requests.post(URL+"sendMessage",json=payload)
    except:
        pass

# ================= API =================

def updates(offset):

    try:
        r=requests.get(URL+"getUpdates",params={"offset":offset,"timeout":25})
        return r.json()
    except:
        return {}

# ================= PRICE =================

def price(coin):

    try:

        r=requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={"ids":coin,"vs_currencies":"usd"}
        )

        data=r.json()

        return data[coin]["usd"]

    except:

        return "Unavailable"

# ================= NEWS =================

def bitcoin_news():

    return """
📰 <b>Bitcoin News</b>

🔗 https://www.coindesk.com/tag/bitcoin/

🔗 https://cointelegraph.com/tags/bitcoin

🔗 https://cryptonews.com/news/bitcoin-news/
"""

def market_news():

    return """
📰 <b>Crypto Market News</b>

🔗 https://www.coindesk.com/markets/

🔗 https://cointelegraph.com/tags/cryptocurrency

🔗 https://cryptonews.com/news/
"""

def regulation_news():

    return """
📰 <b>Crypto Regulation News</b>

🔗 https://www.coindesk.com/policy/

🔗 https://cointelegraph.com/tags/regulation
"""

# ================= AI =================

def ai_answer(q):

    return f"""
🤖 AI Assistant

Question:
{q}

Cryptocurrency markets are volatile.

Tips:
• diversify your portfolio
• manage risk carefully
• always research before investing
"""

# ================= BOT =================

def run():

    offset=0

    while True:

        data=updates(offset)

        if "result" in data:

            for u in data["result"]:

                offset=u["update_id"]+1

                if "message" not in u:
                    continue

                msg=u["message"]
                chat=msg["chat"]["id"]
                text=msg.get("text","").strip()

# START

                if text=="/start":

                    send(chat,
"""
🤖 <b>Crypto AI Assistant</b>

Welcome to your complete cryptocurrency learning and market assistant.

Inside this bot you can:

📚 Learn how cryptocurrency and blockchain work  
📈 Discover trading strategies used by professionals  
⚠ Understand risk management techniques  
📊 Study market trends and cycles  
💰 Check live cryptocurrency prices  
📉 Open real trading charts  
🌕 Explore altcoins and ecosystems  
🔒 Learn how staking works  
💼 Build a diversified portfolio  
📰 Read the latest crypto news  
🧠 Ask questions to the AI assistant

Select a section below to start your crypto journey.
""",
main_menu)

# LEARN

                elif text=="📚 Learn":

                    send(chat,
"""
📚 <b>Crypto Learning Center</b>

This section explains the fundamentals of cryptocurrency and blockchain technology.

You will learn how digital currencies work and why they are transforming global finance.
""",
learn_menu)

                elif text=="What is Crypto":

                    send(chat,
"""
Cryptocurrency is a digital currency secured by cryptography.

It runs on decentralized blockchain networks instead of central banks.

Key advantages:

• global access
• transparency
• decentralization
• security
""",
back_menu)

                elif text=="Blockchain":

                    send(chat,
"""
Blockchain is a distributed digital ledger that records transactions across many computers.

Each block stores verified transactions and connects to the previous block creating a secure chain.
""",
back_menu)

                elif text=="Bitcoin":

                    send(chat,
"""
Bitcoin is the first cryptocurrency created in 2009.

It allows peer-to-peer payments without banks and has a maximum supply of 21 million coins.
""",
back_menu)

                elif text=="Wallets":

                    send(chat,
"""
Crypto wallets store private keys that allow you to access your cryptocurrencies.

Types:

• hot wallets
• cold wallets
""",
back_menu)

                elif text=="DeFi":

                    send(chat,
"""
DeFi stands for Decentralized Finance.

It provides financial services like lending, borrowing and trading without banks.
""",
back_menu)

# TRADING

                elif text=="📈 Trading":

                    send(chat,
"""
📈 <b>Crypto Trading</b>

Trading involves buying and selling cryptocurrencies to profit from price movements.
""",
trading_menu)

                elif text=="Spot Trading":

                    send(chat,"Spot trading means buying real crypto assets instantly.",back_menu)

                elif text=="Futures Trading":

                    send(chat,"Futures trading allows speculation on future prices using leverage.",back_menu)

                elif text=="Technical Analysis":

                    send(chat,"Technical analysis studies price charts and indicators.",back_menu)

                elif text=="Trading Strategies":

                    send(chat,"Strategies include day trading, swing trading and scalping.",back_menu)

# RISK

                elif text=="⚠ Risk":

                    send(chat,
"""
⚠ <b>Risk Management</b>

Managing risk protects your trading capital.
""",
risk_menu)

                elif text=="Stop Loss":

                    send(chat,"A stop loss automatically closes a trade to limit losses.",back_menu)

                elif text=="Risk Reward":

                    send(chat,"Risk reward ratio compares potential profit vs potential loss.",back_menu)

                elif text=="Position Size":

                    send(chat,"Position sizing determines how much capital is used per trade.",back_menu)

# MARKET

                elif text=="📊 Market":

                    send(chat,
"""
📊 <b>Crypto Market Cycles</b>

Markets move through repeating cycles influenced by supply and demand.
""",
market_menu)

                elif text=="Bull Market":

                    send(chat,"A bull market is a period of rising prices and optimism.",back_menu)

                elif text=="Bear Market":

                    send(chat,"A bear market is a prolonged decline in prices.",back_menu)

                elif text=="Market Cycle":

                    send(chat,"Cycles include accumulation, uptrend, distribution and downtrend.",back_menu)

# PRICE

                elif text=="💰 Price":
                    send(chat,"Choose coin:",price_menu)

                elif text=="BTC":
                    send(chat,f"Bitcoin price: ${price('bitcoin')}")

                elif text=="ETH":
                    send(chat,f"Ethereum price: ${price('ethereum')}")

                elif text=="BNB":
                    send(chat,f"BNB price: ${price('binancecoin')}")

                elif text=="SOL":
                    send(chat,f"Solana price: ${price('solana')}")

# CHARTS

                elif text=="📉 Charts":
                    send(chat,"Open chart:",chart_menu)

                elif text=="BTC Chart":
                    send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT")

                elif text=="ETH Chart":
                    send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:ETHUSDT")

                elif text=="BNB Chart":
                    send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:BNBUSDT")

                elif text=="SOL Chart":
                    send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:SOLUSDT")

# ALTCOINS

                elif text=="🌕 Altcoins":
                    send(chat,"Altcoins are cryptocurrencies other than Bitcoin.",alt_menu)

                elif text=="Ethereum":
                    send(chat,"Ethereum enables smart contracts and decentralized apps.",back_menu)

                elif text=="Solana":
                    send(chat,"Solana is a high-speed blockchain with low transaction fees.",back_menu)

                elif text=="Cardano":
                    send(chat,"Cardano focuses on research-driven blockchain development.",back_menu)

# STAKING

                elif text=="🔒 Staking":
                    send(chat,"Learn how staking works.",staking_menu)

                elif text=="What is Staking":
                    send(chat,"Staking locks crypto to support network security.",back_menu)

                elif text=="Staking Rewards":
                    send(chat,"Participants earn rewards for validating transactions.",back_menu)

                elif text=="Staking Risks":
                    send(chat,"Risks include price volatility and lock periods.",back_menu)

# PORTFOLIO

                elif text=="💼 Portfolio":
                    send(chat,"Portfolio management basics.",portfolio_menu)

                elif text=="Diversification":
                    send(chat,"Diversification spreads investment across assets.",back_menu)

                elif text=="Long Term Strategy":
                    send(chat,"Long term investors hold assets for years.",back_menu)

                elif text=="Portfolio Example":
                    send(chat,"Example: 50% BTC, 30% ETH, 20% Altcoins.",back_menu)

# NEWS

                elif text=="📰 News":
                    send(chat,"Choose category:",news_menu)

                elif text=="Bitcoin News":
                    send(chat,bitcoin_news())

                elif text=="Market News":
                    send(chat,market_news())

                elif text=="Regulation News":
                    send(chat,regulation_news())

# AI

                elif text=="🧠 AI Assistant":

                    ai_mode[chat]=True
                    send(chat,"Ask a crypto question.",back_menu)

                elif text=="⬅ Back":

                    ai_mode.pop(chat,None)
                    send(chat,"Main menu",main_menu)

                else:

                    if ai_mode.get(chat):

                        send(chat,ai_answer(text))

                    else:

                        send(chat,"Choose option from menu.",main_menu)

        time.sleep(1)

# START

if __name__=="__main__":

    t=threading.Thread(target=run)
    t.start()

    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
