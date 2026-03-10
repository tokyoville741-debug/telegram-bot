import os
import requests
import threading
import time
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

ai_mode={}
webhook_set=False


# ================= SEND MESSAGE =================

def send(chat,text,keyboard=None):

    data={
        "chat_id":chat,
        "text":text
    }

    if keyboard:
        data["reply_markup"]={
            "keyboard":keyboard,
            "resize_keyboard":True
        }

    requests.post(URL+"/sendMessage",json=data)



# ================= MAIN MENU =================

main_menu=[
["1 Learn","2 Trading"],
["3 Risk","4 Market"],
["5 Price","6 Charts"],
["7 Altcoins","8 Staking"],
["9 Portfolio","10 News"],
["11 AI Assistant"],
["Language"]
]


# ================= SUB MENUS =================

learn_menu=[
["1.1 What is Blockchain"],
["1.2 What is Bitcoin"],
["1.3 What is Ethereum"],
["⬅ Back"]
]

trading_menu=[
["2.1 Spot Trading"],
["2.2 Futures Trading"],
["2.3 Technical Analysis"],
["⬅ Back"]
]

risk_menu=[
["3.1 Risk Management"],
["3.2 Stop Loss"],
["3.3 Position Size"],
["⬅ Back"]
]

market_menu=[
["4.1 Bull Market"],
["4.2 Bear Market"],
["4.3 Market Cycle"],
["⬅ Back"]
]

price_menu=[
["5.1 BTC Price","5.2 ETH Price"],
["5.3 BNB Price","5.4 SOL Price"],
["⬅ Back"]
]

charts_menu=[
["6.1 BTC Chart","6.2 ETH Chart"],
["6.3 BNB Chart","6.4 SOL Chart"],
["⬅ Back"]
]

altcoins_menu=[
["7.1 What are Altcoins"],
["7.2 Popular Altcoins"],
["7.3 Altcoin Season"],
["⬅ Back"]
]

staking_menu=[
["8.1 What is Staking"],
["8.2 Staking Rewards"],
["8.3 Proof of Stake"],
["⬅ Back"]
]

portfolio_menu=[
["9.1 Diversification"],
["9.2 Long Term Investing"],
["9.3 Portfolio Tracking"],
["9.4 Rebalancing"],
["⬅ Back"]
]

news_menu=[
["10.1 CoinDesk"],
["10.2 CoinTelegraph"],
["10.3 Decrypt"],
["10.4 Binance News"],
["⬅ Back"]
]

language_menu=[
["English","Français"],
["Español"],
["⬅ Back"]
]


# ================= PRICE FUNCTION =================

def get_price(symbol):

    try:
        r=requests.get(
        f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        )
        return r.json()["price"]

    except:
        return "Unavailable"



# ================= EDUCATIONAL TEXTS =================

BLOCKCHAIN_TEXT = """⛓ WHAT IS BLOCKCHAIN?

Blockchain is a decentralized digital ledger technology that records transactions across many computers in a secure and transparent way.

Each transaction is grouped into a block. Once verified, it is linked to the previous block forming a chain.

Blockchain provides decentralization, transparency and strong cryptographic security.
"""

BITCOIN_TEXT = """₿ WHAT IS BITCOIN?

Bitcoin is the first cryptocurrency created in 2009 by Satoshi Nakamoto.

It allows people to send digital money without banks.

Only 21 million bitcoins will ever exist which makes it scarce and often compared to digital gold.
"""

ETHEREUM_TEXT = """💎 WHAT IS ETHEREUM?

Ethereum is a programmable blockchain that allows developers to build decentralized applications.

It introduced smart contracts which automatically execute agreements on the blockchain.
"""

SPOT_TRADING_TEXT = """📊 SPOT TRADING

Spot trading means buying or selling crypto at the current market price.

The asset is delivered instantly to your account.
"""

FUTURES_TRADING_TEXT = """📈 FUTURES TRADING

Futures trading allows traders to speculate on price movements without owning the asset.

It often involves leverage which increases both profits and risks.
"""

TECHNICAL_ANALYSIS_TEXT = """📉 TECHNICAL ANALYSIS

Technical analysis studies charts and historical price data to predict market movements.
"""

RISK_MANAGEMENT_TEXT = """⚠ RISK MANAGEMENT

Risk management helps traders protect capital by controlling position size and using stop losses.
"""

STOP_LOSS_TEXT = """🛑 STOP LOSS

A stop loss automatically closes a trade when the price reaches a specific level.
"""

POSITION_SIZE_TEXT = """📏 POSITION SIZE

Position sizing controls how much capital you risk on each trade.
"""



# ================= BOT =================

@app.route(f"/{TOKEN}", methods=["POST"])
def bot():

    data = request.get_json()

    if not data or "message" not in data:
        return "ok"

    chat = data["message"]["chat"]["id"]
    text = data["message"].get("text","")



# ================= START =================

    if text=="/start":

        ai_mode[chat]=False

        send(chat,
        "🚀 Welcome to OpenClaw AI Coach\n\n"
        "Your intelligent assistant for learning and exploring the world of cryptocurrency.",
        main_menu)



# ================= BACK =================

    elif text=="⬅ Back":

        ai_mode[chat]=False
        send(chat,"Main Menu",main_menu)



# ================= LEARN =================

    elif text=="1 Learn":
        send(chat,"Crypto learning section.",learn_menu)

    elif text=="1.1 What is Blockchain":
        send(chat,BLOCKCHAIN_TEXT)

    elif text=="1.2 What is Bitcoin":
        send(chat,BITCOIN_TEXT)

    elif text=="1.3 What is Ethereum":
        send(chat,ETHEREUM_TEXT)



# ================= TRADING =================

    elif text=="2 Trading":
        send(chat,"Trading section.",trading_menu)

    elif text=="2.1 Spot Trading":
        send(chat,SPOT_TRADING_TEXT)

    elif text=="2.2 Futures Trading":
        send(chat,FUTURES_TRADING_TEXT)

    elif text=="2.3 Technical Analysis":
        send(chat,TECHNICAL_ANALYSIS_TEXT)



# ================= RISK =================

    elif text=="3 Risk":
        send(chat,"Risk management.",risk_menu)

    elif text=="3.1 Risk Management":
        send(chat,RISK_MANAGEMENT_TEXT)

    elif text=="3.2 Stop Loss":
        send(chat,STOP_LOSS_TEXT)

    elif text=="3.3 Position Size":
        send(chat,POSITION_SIZE_TEXT)



# ================= PRICE =================

    elif text=="5 Price":
        send(chat,"Select a cryptocurrency.",price_menu)

    elif text=="5.1 BTC Price":
        price=get_price("BTCUSDT")
        send(chat,f"BTC Price: ${price}")

    elif text=="5.2 ETH Price":
        price=get_price("ETHUSDT")
        send(chat,f"ETH Price: ${price}")



# ================= AI ASSISTANT =================

    elif text=="11 AI Assistant":

        ai_mode[chat]=True

        send(chat,
        "🤖 AI Assistant Activated\n\n"
        "Ask any question about cryptocurrency.")



# ================= AI RESPONSE =================

    elif ai_mode.get(chat):

        try:

            r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
            "Authorization":f"Bearer {GROQ_API_KEY}",
            "Content-Type":"application/json"
            },
            json={
            "model":"llama3-70b-8192",
            "messages":[
            {"role":"user","content":text}
            ]
            })

            result=r.json()

            if "choices" in result:
                reply=result["choices"][0]["message"]["content"]
                send(chat,reply[:4000])
            else:
                send(chat,"⚠ AI error")

        except Exception as e:
            send(chat,"⚠ AI unavailable.")


    return "ok"



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
