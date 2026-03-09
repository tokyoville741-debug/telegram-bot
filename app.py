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
# LANGUAGE SYSTEM
# =========================

languages={}

language_menu={
"keyboard":[
["🇬🇧 English","🇫🇷 Français"],
["🇪🇸 Español"],
["⬅ Back"]
],
"resize_keyboard":True
}


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
["🧠 AI Assistant"],
["🌍 Language"]
],
"resize_keyboard":True
}


# =========================
# SUB MENUS
# =========================

trading_menu={
"keyboard":[
["1️⃣ Day Trading"],
["2️⃣ Swing Trading"],
["3️⃣ Long-term Investing"],
["⬅ Back"]
],
"resize_keyboard":True
}

market_menu={
"keyboard":[
["1️⃣ Accumulation"],
["2️⃣ Uptrend"],
["3️⃣ Distribution"],
["4️⃣ Downtrend"],
["⬅ Back"]
],
"resize_keyboard":True
}

staking_menu={
"keyboard":[
["1️⃣ Passive income"],
["2️⃣ Network security"],
["3️⃣ Long-term investment strategy"],
["⬅ Back"]
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
# CHART MENU
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
# NEWS
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


            # START

            if text=="/start":

                welcome="""
🤖 Welcome to the Crypto AI Assistant

This bot helps you learn cryptocurrency step by step.
"""

                send(chat,welcome,main_menu)


            # TRADING

            elif text=="2️⃣ 📈 Trading":

                send(chat,
"""
📈 WHAT IS CRYPTO TRADING?

Crypto trading is the act of buying and selling cryptocurrencies in order to make a profit.

Traders analyze price movements using charts and market data.
""",
                trading_menu)


            elif text=="1️⃣ Day Trading":

                send(chat,
"""
📈 DAY TRADING

Buying and selling crypto within the same day to profit from short-term price movements.
""",
                back_menu)


            elif text=="2️⃣ Swing Trading":

                send(chat,
"""
📊 SWING TRADING

Holding trades for several days or weeks to capture market trends.
""",
                back_menu)


            elif text=="3️⃣ Long-term Investing":

                send(chat,
"""
🪙 LONG TERM INVESTING

Holding crypto for months or years expecting long term growth.
""",
                back_menu)


            # MARKET

            elif text=="4️⃣ 📊 Market":

                send(chat,
"""
📊 CRYPTO MARKET CYCLES

Markets move in repeating phases driven by investor psychology.
""",
                market_menu)


            elif text=="1️⃣ Accumulation":

                send(chat,
"""
Accumulation phase happens after a market crash where smart investors slowly buy assets.
""",
                back_menu)


            elif text=="2️⃣ Uptrend":

                send(chat,
"""
Uptrend phase is when prices start rising and investor confidence returns.
""",
                back_menu)


            elif text=="3️⃣ Distribution":

                send(chat,
"""
Distribution phase is when early investors start taking profits.
""",
                back_menu)


            elif text=="4️⃣ Downtrend":

                send(chat,
"""
Downtrend is when selling pressure dominates and prices fall.
""",
                back_menu)


            # STAKING

            elif text=="8️⃣ 🔒 Staking":

                send(chat,
"""
🔒 WHAT IS STAKING?

Staking allows crypto holders to earn rewards by locking their coins to support a blockchain network.

Benefits:

• Passive income
• Network security
• Long-term investment strategy
""",
                staking_menu)


            elif text=="1️⃣ Passive income":

                send(chat,
"""
Passive income means earning rewards regularly just by holding and staking your crypto.
""",
                back_menu)


            elif text=="2️⃣ Network security":

                send(chat,
"""
Staking helps validate blockchain transactions and keeps the network secure.
""",
                back_menu)


            elif text=="3️⃣ Long-term investment strategy":

                send(chat,
"""
Staking encourages holding crypto long term while earning rewards.
""",
                back_menu)


            # PRICE

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


            # CHARTS

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


            # BACK

            elif text=="⬅ Back":
                send(chat,"Main menu",main_menu)

        time.sleep(1)


# START BOT

if __name__=="__main__":

    bot_thread=threading.Thread(target=run_bot)
    bot_thread.start()

    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
