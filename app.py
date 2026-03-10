import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}"

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

user_lang = {}
webhook_set = False
ai_mode = {}

# ===================== MENUS =====================

main_menu = {
"keyboard":[
["1️⃣ Learn","2️⃣ Trading"],
["3️⃣ Risk","4️⃣ Market"],
["5️⃣ Price","6️⃣ Charts"],
["7️⃣ Altcoins","8️⃣ Staking"],
["9️⃣ Portfolio","🔟 News"],
["1️⃣1️⃣ AI Assistant","🌐 Language"]
],
"resize_keyboard":True
}

learn_menu = {
"keyboard":[
["1.1 Blockchain","1.2 Bitcoin"],
["1.3 Wallet","1.4 DeFi"],
["⬅ Back"]
],
"resize_keyboard":True
}

trading_menu = {
"keyboard":[
["2.1 Spot Trading","2.2 Futures"],
["2.3 Day Trading","2.4 Swing Trading"],
["⬅ Back"]
],
"resize_keyboard":True
}

risk_menu = {
"keyboard":[
["3.1 Stop Loss","3.2 Position Size"],
["3.3 Risk Reward","3.4 Diversification"],
["⬅ Back"]
],
"resize_keyboard":True
}

market_menu = {
"keyboard":[
["4.1 Bull Market","4.2 Bear Market"],
["4.3 Market Cap","4.4 Liquidity"],
["⬅ Back"]
],
"resize_keyboard":True
}

price_menu = {
"keyboard":[
["5.1 BTC","5.2 ETH"],
["5.3 BNB","5.4 SOL"],
["⬅ Back"]
],
"resize_keyboard":True
}

chart_menu = {
"keyboard":[
["6.1 BTC Chart","6.2 ETH Chart"],
["6.3 BNB Chart","6.4 SOL Chart"],
["⬅ Back"]
],
"resize_keyboard":True
}

alt_menu = {
"keyboard":[
["7.1 Ethereum","7.2 Solana"],
["7.3 Cardano","7.4 Polkadot"],
["⬅ Back"]
],
"resize_keyboard":True
}

staking_menu = {
"keyboard":[
["8.1 What is Staking","8.2 Proof of Stake"],
["8.3 Staking Rewards","8.4 Staking Risks"],
["⬅ Back"]
],
"resize_keyboard":True
}

portfolio_menu = {
"keyboard":[
["9.1 Diversification","9.2 Long Term Investing"],
["9.3 Portfolio Tracking","9.4 Rebalancing"],
["⬅ Back"]
],
"resize_keyboard":True
}

news_menu = {
"keyboard":[
["10.1 CoinDesk","10.2 CoinTelegraph"],
["10.3 Decrypt","10.4 Binance News"],
["⬅ Back"]
],
"resize_keyboard":True
}

language_menu={
"keyboard":[
["English 🇺🇸"],
["Français 🇫🇷"],
["Español 🇪🇸"],
["⬅ Back"]
],
"resize_keyboard":True
}

# ===================== SEND =====================

def send(chat,text,menu=None):

    payload={
    "chat_id":chat,
    "text":text
    }

    if menu:
        payload["reply_markup"]=menu

    requests.post(URL+"/sendMessage",json=payload)

# ===================== PRICE =====================

def price(coin):
    try:
        r = requests.get(
            f"https://api.coinpaprika.com/v1/tickers/{coin}",
            timeout=10
        )

        if r.status_code != 200:
            return "Unavailable"

        data = r.json()

        price = data["quotes"]["USD"]["price"]

        return round(price,2)

    except:
        return "Unavailable"

# ===================== WEB =====================

@app.route("/",methods=["GET"])
def home():
    return "Bot running"

@app.route(f"/{TOKEN}",methods=["POST"])
def bot():

    data=request.json

    if "message" in data:

        chat=data["message"]["chat"]["id"]
        text=data["message"].get("text","")

        if chat not in user_lang:
            user_lang[chat]="EN"

# ===================== START =====================

        if text=="/start":

            send(chat,
            "Welcome to the Crypto Education Bot.\n\n"
            "This bot teaches cryptocurrency, blockchain, trading strategies, "
            "risk management, market analysis and portfolio management.\n\n"
            "Each section contains numbered lessons and detailed explanations.\n"
            "Select a topic from the menu below to start learning.",
            main_menu)

# ===================== LANGUAGE =====================

        elif text=="🌐 Language":

            send(chat,
            "Choose your preferred language.",
            language_menu)

        elif text=="English 🇺🇸":

            user_lang[chat]="EN"
            send(chat,"Language changed to English.",main_menu)

        elif text=="Français 🇫🇷":

            user_lang[chat]="FR"
            send(chat,"Langue changée en Français.",main_menu)

        elif text=="Español 🇪🇸":

            user_lang[chat]="ES"
            send(chat,"Idioma cambiado a Español.",main_menu)

# ===================== LEARN =====================

        elif text=="1️⃣ Learn":

            send(chat,
            "1️⃣ Learn - Crypto Fundamentals\n\n"
            "This section introduces the core concepts of cryptocurrency. "
            "You will learn how blockchain works, what Bitcoin is, "
            "how wallets store crypto and how decentralized finance operates.",
            learn_menu)

        elif text=="1.1 Blockchain":

            send(chat,
            "1.1 Blockchain\n\n"
            "Blockchain is a decentralized digital ledger that records "
            "transactions across many computers in a secure and transparent way.",
            learn_menu)

        elif text=="1.2 Bitcoin":

            send(chat,
            "1.2 Bitcoin\n\n"
            "Bitcoin is the first cryptocurrency created in 2009 by "
            "Satoshi Nakamoto. It allows peer-to-peer payments without banks.",
            learn_menu)

        elif text=="1.3 Wallet":

            send(chat,
            "1.3 Wallet\n\n"
            "A crypto wallet stores private keys used to access and "
            "manage cryptocurrency assets securely.",
            learn_menu)

        elif text=="1.4 DeFi":

            send(chat,
            "1.4 DeFi\n\n"
            "Decentralized Finance allows lending, borrowing, trading "
            "and earning interest without traditional banks.",
            learn_menu)

# ===================== TRADING =====================

        elif text=="2️⃣ Trading":

            send(chat,
            "2️⃣ Trading\n\n"
            "Crypto trading involves buying and selling digital assets "
            "to profit from market price movements.",
            trading_menu)

        elif text=="2.1 Spot Trading":

            send(chat,
            "2.1 Spot Trading\n\n"
            "Spot trading means buying and selling assets instantly "
            "at the current market price.",
            trading_menu)

        elif text=="2.2 Futures":

            send(chat,
            "2.2 Futures Trading\n\n"
            "Futures contracts allow traders to speculate on the future "
            "price of an asset using leverage.",
            trading_menu)

        elif text=="2.3 Day Trading":

            send(chat,
            "2.3 Day Trading\n\n"
            "Day traders open and close positions within the same day "
            "to capture small market movements.",
            trading_menu)

        elif text=="2.4 Swing Trading":

            send(chat,
            "2.4 Swing Trading\n\n"
            "Swing trading holds positions for several days or weeks "
            "to capture medium-term price trends.",
            trading_menu)

# ===================== RISK =====================

        elif text=="3️⃣ Risk":

            send(chat,
            "3️⃣ Risk Management\n\n"
            "Risk management helps protect your trading capital "
            "and control potential losses.",
            risk_menu)

        elif text=="3.1 Stop Loss":

            send(chat,
            "3.1 Stop Loss\n\n"
            "A stop loss automatically closes a trade "
            "when price reaches a certain level.",
            risk_menu)

        elif text=="3.2 Position Size":

            send(chat,
            "3.2 Position Size\n\n"
            "Position sizing determines how much capital "
            "you allocate to a single trade.",
            risk_menu)

        elif text=="3.3 Risk Reward":

            send(chat,
            "3.3 Risk Reward\n\n"
            "The risk-reward ratio compares potential profit "
            "to potential loss.",
            risk_menu)

        elif text=="3.4 Diversification":

            send(chat,
            "3.4 Diversification\n\n"
            "Diversifying investments across different assets "
            "helps reduce overall portfolio risk.",
            risk_menu)

# ===================== MARKET =====================

        elif text=="4️⃣ Market":

            send(chat,
            "4️⃣ Crypto Market\n\n"
            "The crypto market consists of thousands of "
            "digital assets traded worldwide.",
            market_menu)

        elif text=="4.1 Bull Market":

            send(chat,
            "4.1 Bull Market\n\n"
            "A bull market occurs when prices rise "
            "and investor confidence increases.",
            market_menu)

        elif text=="4.2 Bear Market":

            send(chat,
            "4.2 Bear Market\n\n"
            "A bear market occurs when prices decline "
            "for a prolonged period.",
            market_menu)

        elif text=="4.3 Market Cap":

            send(chat,
            "4.3 Market Capitalization\n\n"
            "Market cap represents the total value "
            "of a cryptocurrency.",
            market_menu)

        elif text=="4.4 Liquidity":

            send(chat,
            "4.4 Liquidity\n\n"
            "Liquidity indicates how easily an asset "
            "can be bought or sold without affecting price.",
            market_menu)

# ===================== PRICE =====================

        elif text=="5️⃣ Price":

            send(chat,
            "5️⃣ Cryptocurrency Prices\n\n"
            "Select a cryptocurrency to check "
            "its current market price.",
            price_menu)

        elif text=="5.1 BTC":

            send(chat,f"Bitcoin Price: ${price('btc-bitcoin')}")

        elif text=="5.2 ETH":

            send(chat,f"Ethereum Price: ${price('eth-ethereum')}")

        elif text=="5.3 BNB":

            send(chat,f"BNB Price: ${price('bnb-binance-coin')}")

        elif text=="5.4 SOL":

            send(chat,f"Solana Price: ${price('sol-solana')}")

# ===================== AI =====================

        elif text=="1️⃣1️⃣ AI Assistant":

            ai_mode[chat]=True

            send(chat,
            "1️⃣1️⃣ AI Assistant\n\n"
            "Ask any cryptocurrency question.")

        elif chat in ai_mode and ai_mode[chat]:

            try:

                r=requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                "Authorization":f"Bearer {GROQ_API_KEY}",
                "Content-Type":"application/json"
                },
                json={
                "model":"llama-3.3-70b-versatile",
                "messages":[
                {"role":"system","content":"You are a crypto expert assistant."},
                {"role":"user","content":text}
                ]
                })

                answer=r.json()["choices"][0]["message"]["content"]

                send(chat,answer)

            except:

                send(chat,"AI service unavailable.")

# ===================== BACK =====================

        elif text=="⬅ Back":

            ai_mode[chat]=False
            send(chat,"Main Menu",main_menu)

    return "ok"

# ===================== WEBHOOK =====================

@app.before_request
def setup_webhook():

    global webhook_set

    if not webhook_set:

        url=os.environ.get("RENDER_EXTERNAL_URL")+f"/{TOKEN}"

        requests.get(URL+"/setWebhook",params={"url":url})

        webhook_set=True

# ===================== RUN =====================

if __name__=="__main__":

    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
