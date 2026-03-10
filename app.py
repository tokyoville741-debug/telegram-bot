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

# ================= EDUCATION TEXTS =================

BLOCKCHAIN_TEXT="Blockchain is a decentralized ledger used to record transactions securely."

BITCOIN_TEXT="Bitcoin is the first cryptocurrency created in 2009 by Satoshi Nakamoto."

ETHEREUM_TEXT="Ethereum is a blockchain platform allowing smart contracts and decentralized apps."

SPOT_TRADING_TEXT="Spot trading means buying or selling crypto instantly at market price."

FUTURES_TRADING_TEXT="Futures trading allows speculation on price movements with leverage."

TECHNICAL_ANALYSIS_TEXT="Technical analysis studies price charts to predict market movements."

RISK_MANAGEMENT_TEXT="Risk management protects traders from large losses."

STOP_LOSS_TEXT="A stop loss automatically closes a trade when price hits a specific level."

POSITION_SIZE_TEXT="Position sizing controls how much capital is used in each trade."

BULL_MARKET="A bull market is a period where prices are rising."

BEAR_MARKET="A bear market is a period where prices are falling."

MARKET_CYCLE="Market cycles include accumulation, uptrend, distribution and downtrend."

ALTCOINS_TEXT="Altcoins are cryptocurrencies other than Bitcoin."

POPULAR_ALTCOINS="Popular altcoins include ETH, BNB, SOL, XRP."

ALTCOIN_SEASON="Altcoin season occurs when altcoins outperform Bitcoin."

STAKING_TEXT="Staking allows users to earn rewards by locking crypto."

STAKING_REWARDS="Staking rewards are incentives for securing PoS networks."

PROOF_OF_STAKE="Proof of Stake is a consensus mechanism replacing mining."

DIVERSIFICATION="Diversification spreads investments across assets."

LONG_TERM="Long term investing means holding assets for years."

PORTFOLIO_TRACK="Portfolio tracking helps monitor investments."

REBALANCING="Rebalancing adjusts asset allocations."

COINDESK="https://coindesk.com"

COINTELEGRAPH="https://cointelegraph.com"

DECRYPT="https://decrypt.co"

BINANCE_NEWS="https://www.binance.com/en/news"

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
"👇 Select a topic from the menu below.",
main_menu)

# ================= BACK =================

    elif text=="⬅ Back":
        ai_mode[chat]=False
        send(chat,"Main Menu",main_menu)

# ================= MENUS =================

    elif text=="1 Learn":
        send(chat,"Learning Section",learn_menu)

    elif text=="2 Trading":
        send(chat,"Trading Section",trading_menu)

    elif text=="3 Risk":
        send(chat,"Risk Section",risk_menu)

    elif text=="4 Market":
        send(chat,"Market Section",market_menu)

    elif text=="5 Price":
        send(chat,"Select crypto",price_menu)

    elif text=="6 Charts":
        send(chat,"Charts coming soon")

    elif text=="7 Altcoins":
        send(chat,"Altcoins Section",altcoins_menu)

    elif text=="8 Staking":
        send(chat,"Staking Section",staking_menu)

    elif text=="9 Portfolio":
        send(chat,"Portfolio Section",portfolio_menu)

    elif text=="10 News":
        send(chat,"News Sources",news_menu)

# ================= CONTENT =================

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

    elif text=="4.1 Bull Market":
        send(chat,BULL_MARKET)

    elif text=="4.2 Bear Market":
        send(chat,BEAR_MARKET)

    elif text=="4.3 Market Cycle":
        send(chat,MARKET_CYCLE)

    elif text=="7.1 What are Altcoins":
        send(chat,ALTCOINS_TEXT)

    elif text=="7.2 Popular Altcoins":
        send(chat,POPULAR_ALTCOINS)

    elif text=="7.3 Altcoin Season":
        send(chat,ALTCOIN_SEASON)

    elif text=="8.1 What is Staking":
        send(chat,STAKING_TEXT)

    elif text=="8.2 Staking Rewards":
        send(chat,STAKING_REWARDS)

    elif text=="8.3 Proof of Stake":
        send(chat,PROOF_OF_STAKE)

    elif text=="9.1 Diversification":
        send(chat,DIVERSIFICATION)

    elif text=="9.2 Long Term Investing":
        send(chat,LONG_TERM)

    elif text=="9.3 Portfolio Tracking":
        send(chat,PORTFOLIO_TRACK)

    elif text=="9.4 Rebalancing":
        send(chat,REBALANCING)

    elif text=="10.1 CoinDesk":
        send(chat,COINDESK)

    elif text=="10.2 CoinTelegraph":
        send(chat,COINTELEGRAPH)

    elif text=="10.3 Decrypt":
        send(chat,DECRYPT)

    elif text=="10.4 Binance News":
        send(chat,BINANCE_NEWS)

# ================= PRICES =================

    elif text=="5.1 BTC Price":
        send(chat,f"BTC Price: ${get_price('BTCUSDT')}")

    elif text=="5.2 ETH Price":
        send(chat,f"ETH Price: ${get_price('ETHUSDT')}")

    elif text=="5.3 BNB Price":
        send(chat,f"BNB Price: ${get_price('BNBUSDT')}")

    elif text=="5.4 SOL Price":
        send(chat,f"SOL Price: ${get_price('SOLUSDT')}")

# ================= AI =================

    elif text=="11 AI Assistant":

        ai_mode[chat]=True

        send(chat,"🤖 AI Assistant Activated\nAsk anything about crypto.")

    elif ai_mode.get(chat):

        try:

            r=requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
            "Authorization":f"Bearer {GROQ_API_KEY}",
            "Content-Type":"application/json"
            },
            json={
            "model":"llama3-8b-8192",
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
