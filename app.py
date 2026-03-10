import os
import requests
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

ai_mode={}


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
        r=requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
        return r.json()["price"]
    except:
        return "Unavailable"


# ================= EDUCATIONAL TEXTS =================

BLOCKCHAIN_TEXT="""⛓ WHAT IS BLOCKCHAIN?

Blockchain is a decentralized digital ledger technology that records transactions across many computers in a secure and transparent way.

Each transaction is grouped into a block. Once verified it is linked to the previous block forming a chain.

Blockchain provides decentralization, transparency and strong cryptographic security.
"""

BITCOIN_TEXT="""₿ WHAT IS BITCOIN?

Bitcoin is the first cryptocurrency ever created and remains the most widely recognized digital asset in the world. It was introduced in 2009 by an anonymous person or group using the name Satoshi Nakamoto.

The main goal of Bitcoin was to create a decentralized digital currency that allows people to send money directly to each other without needing banks or financial intermediaries.
"""

ETHEREUM_TEXT="""💎 WHAT IS ETHEREUM?

Ethereum is a blockchain platform that allows developers to build decentralized applications known as dApps.

One of Ethereum's most important innovations is the concept of smart contracts.
"""

SPOT_TRADING_TEXT="""📊 SPOT TRADING

Spot trading means buying or selling crypto at the current market price.

The asset is delivered instantly to your account.
"""

FUTURES_TRADING_TEXT="""📈 FUTURES TRADING

Futures trading allows traders to speculate on the future price of crypto without owning the asset.
"""

TECHNICAL_ANALYSIS_TEXT="""📉 TECHNICAL ANALYSIS

Technical analysis studies charts and historical price data to predict market movements.
"""

RISK_MANAGEMENT_TEXT="""⚠ RISK MANAGEMENT

Risk management helps traders protect capital and minimize losses.
"""

STOP_LOSS_TEXT="""🛑 STOP LOSS

A stop loss automatically closes a trade when price reaches a specific level.
"""

POSITION_SIZE_TEXT="""📏 POSITION SIZE

Position sizing determines how much capital you risk in a trade.
"""


# ================= BOT =================

@app.route(f"/{TOKEN}",methods=["POST"])
def bot():

    data=request.get_json()

    if not data or "message" not in data:
        return "ok"

    chat=data["message"]["chat"]["id"]
    text=data["message"].get("text","")



# ================= START =================

    if text=="/start":

        ai_mode[chat]=False

        send(chat,
"🚀 Welcome to OpenClaw AI Coach\n\n"
"Your intelligent assistant for learning and exploring the world of cryptocurrency, trading, and blockchain technology.\n\n"
"With OpenClaw AI Coach you can:\n"
"📚 Learn crypto fundamentals\n"
"📊 Understand trading strategies\n"
"📉 Discover risk management techniques\n"
"📈 Explore crypto charts\n"
"🪙 Learn about altcoins\n"
"💰 Understand staking and passive income\n"
"📰 Stay updated with crypto news\n"
"🤖 Ask the AI Assistant any question\n\n"
"Whether you are a beginner or an experienced trader, this bot will help you understand the crypto ecosystem step by step.\n\n"
"👇 Select a topic from the menu below.",
main_menu)



# ================= BACK =================

    elif text=="⬅ Back":

        ai_mode[chat]=False
        send(chat,"Main Menu",main_menu)



# ================= MENUS =================

    elif text=="1 Learn":
        send(chat,"Crypto Learning",learn_menu)

    elif text=="2 Trading":
        send(chat,"Trading Section",trading_menu)

    elif text=="3 Risk":
        send(chat,"Risk Section",risk_menu)

    elif text=="4 Market":
        send(chat,"Market Section",market_menu)

    elif text=="5 Price":
        send(chat,"Select a cryptocurrency.",price_menu)

    elif text=="6 Charts":
        send(chat,"Charts Section",charts_menu)

    elif text=="7 Altcoins":
        send(chat,"Altcoins Section",altcoins_menu)

    elif text=="8 Staking":
        send(chat,"Staking Section",staking_menu)

    elif text=="9 Portfolio":
        send(chat,"Portfolio Section",portfolio_menu)

    elif text=="10 News":
        send(chat,"News Sources",news_menu)



# ================= EDUCATION =================

    elif text=="1.1 What is Blockchain":
        send(chat,BLOCKCHAIN_TEXT)

    elif text=="1.2 What is Bitcoin":
        send(chat,BITCOIN_TEXT)

    elif text=="1.3 What is Ethereum":
        send(chat,ETHEREUM_TEXT)

    elif text=="2.1 Spot Trading":
        send(chat,SPOT_TRADING_TEXT)

    elif text=="2.2 Futures Trading":
        send(chat,FUTURES_TRADING_TEXT)

    elif text=="2.3 Technical Analysis":
        send(chat,TECHNICAL_ANALYSIS_TEXT)

    elif text=="3.1 Risk Management":
        send(chat,RISK_MANAGEMENT_TEXT)

    elif text=="3.2 Stop Loss":
        send(chat,STOP_LOSS_TEXT)

    elif text=="3.3 Position Size":
        send(chat,POSITION_SIZE_TEXT)



# ================= PRICES =================

    elif text=="5.1 BTC Price":
        send(chat,f"BTC Price: ${get_price('BTCUSDT')}")

    elif text=="5.2 ETH Price":
        send(chat,f"ETH Price: ${get_price('ETHUSDT')}")

    elif text=="5.3 BNB Price":
        send(chat,f"BNB Price: ${get_price('BNBUSDT')}")

    elif text=="5.4 SOL Price":
        send(chat,f"SOL Price: ${get_price('SOLUSDT')}")



# ================= LANGUAGE =================

    elif text=="Language":
        send(chat,"Select language",language_menu)

    elif text=="English":
        send(chat,"Language set to English.")

    elif text=="Français":
        send(chat,"Langue définie sur Français.")

    elif text=="Español":
        send(chat,"Idioma configurado en Español.")



# ================= AI ASSISTANT =================

    elif text=="11 AI Assistant":

        ai_mode[chat]=True

        send(chat,
"🤖 AI Assistant Activated\n\n"
"Ask any question about cryptocurrency, trading or blockchain.")



# ================= AI RESPONSE =================

    elif ai_mode.get(chat):

        try:

            r=requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
            "Authorization":f"Bearer {GROQ_API_KEY}",
            "Content-Type":"application/json"
            },
            json={
            "model":"llama3-70b-8192",
            "messages":[{"role":"user","content":text}]
            })

            reply=r.json()["choices"][0]["message"]["content"]

            send(chat,reply[:4000])

        except:

            send(chat,"⚠ AI unavailable.")


    return "ok"



if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
