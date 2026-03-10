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

# ===================== MAIN SECTIONS =====================

        elif text=="1️⃣ Learn":
            send(chat,"1️⃣ Crypto Learning\n\nChoose a lesson.",learn_menu)

        elif text=="2️⃣ Trading":
            send(chat,"2️⃣ Trading Strategies\n\nChoose a lesson.",trading_menu)

        elif text=="3️⃣ Risk":
            send(chat,"3️⃣ Risk Management\n\nChoose a lesson.",risk_menu)

        elif text=="4️⃣ Market":
            send(chat,"4️⃣ Market Analysis\n\nChoose a lesson.",market_menu)

        elif text=="6️⃣ Charts":
            send(chat,"6️⃣ Crypto Charts\n\nSelect a chart.",chart_menu)

        elif text=="7️⃣ Altcoins":
            send(chat,"7️⃣ Altcoins\n\nChoose a coin.",alt_menu)

        elif text=="8️⃣ Staking":
            send(chat,"8️⃣ Staking\n\nChoose a lesson.",staking_menu)

        elif text=="9️⃣ Portfolio":
            send(chat,"9️⃣ Portfolio Management\n\nChoose a lesson.",portfolio_menu)

        elif text=="🔟 News":
            send(chat,"🔟 Crypto News\n\nSelect a source.",news_menu)

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
            "Ask any cryptocurrency question.\n\n"
            "Press ⬅ Back to exit AI mode.",
            main_menu)

        elif chat in ai_mode and ai_mode[chat] and text not in [
        "⬅ Back",
        "1️⃣ Learn","2️⃣ Trading","3️⃣ Risk","4️⃣ Market",
        "5️⃣ Price","6️⃣ Charts","7️⃣ Altcoins","8️⃣ Staking",
        "9️⃣ Portfolio","🔟 News","🌐 Language"]:

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
