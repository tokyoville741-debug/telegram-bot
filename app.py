import requests
import os
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN")
LLAMA_API_KEY = os.environ.get("LLAMA_API_KEY")

URL = f"https://api.telegram.org/bot{TOKEN}/"
WEBHOOK_PATH = f"/{TOKEN}"

app = Flask(__name__)

# =====================
# MENUS
# =====================

main_menu={
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

learn_menu={
"keyboard":[
["1️⃣ What is Crypto"],
["2️⃣ What is Blockchain"],
["3️⃣ What is Bitcoin"],
["⬅ Back"]
],
"resize_keyboard":True
}

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
["3️⃣ Long-term strategy"],
["⬅ Back"]
],
"resize_keyboard":True
}

price_menu={
"keyboard":[
["BTC","ETH"],
["SOL","BNB"],
["⬅ Back"]
],
"resize_keyboard":True
}

chart_menu={
"keyboard":[
["BTC Chart","ETH Chart"],
["SOL Chart","BNB Chart"],
["⬅ Back"]
],
"resize_keyboard":True
}

language_menu={
"keyboard":[
["🇬🇧 English","🇫🇷 Français"],
["🇪🇸 Español"],
["⬅ Back"]
],
"resize_keyboard":True
}

back_menu={"keyboard":[["⬅ Back"]],"resize_keyboard":True}

ai_mode={}

# =====================
# SEND MESSAGE
# =====================

def send(chat_id,text,keyboard=None):

    payload={"chat_id":chat_id,"text":text}

    if keyboard:
        payload["reply_markup"]=keyboard

    requests.post(URL+"sendMessage",json=payload)


# =====================
# PRICE
# =====================

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


# =====================
# NEWS
# =====================

def crypto_news():

    try:

        r=requests.get(
        "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
        )

        news=r.json()["Data"][:5]

        text="📰 Latest Crypto News\n\n"

        for n in news:
            text+=f"{n['title']}\n{n['url']}\n\n"

        return text

    except:
        return "News unavailable."


# =====================
# AI
# =====================

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

    r=requests.post(
    "https://api.llama-api.com/chat/completions",
    headers=headers,
    json=data
    )

    result=r.json()

    return result["choices"][0]["message"]["content"]


# =====================
# TELEGRAM WEBHOOK
# =====================

@app.route(WEBHOOK_PATH,methods=["POST"])
def webhook():

    update=request.json

    if "message" not in update:
        return "ok"

    msg=update["message"]

    if "text" not in msg:
        return "ok"

    chat=msg["chat"]["id"]
    text=msg["text"]


# =====================
# START
# =====================

    if text=="/start":

        send(chat,
"""
🤖 Welcome to Crypto AI Assistant

This bot helps you learn cryptocurrency step by step.

Use the menu below to explore trading, markets,
prices, charts and AI crypto analysis.
""",
        main_menu)


# =====================
# LEARN
# =====================

    elif text=="1️⃣ 📚 Learn":

        send(chat,"Choose a topic",learn_menu)

    elif text=="1️⃣ What is Crypto":

        send(chat,
"""
Cryptocurrency is digital money secured by cryptography.

It runs on decentralized networks called blockchains.
Examples include Bitcoin and Ethereum.
""",
        back_menu)

    elif text=="2️⃣ What is Blockchain":

        send(chat,
"""
Blockchain is a distributed ledger that records
transactions across many computers.

It ensures transparency and security.
""",
        back_menu)

    elif text=="3️⃣ What is Bitcoin":

        send(chat,
"""
Bitcoin is the first cryptocurrency created in 2009.

It allows peer-to-peer payments without banks.
""",
        back_menu)


# =====================
# TRADING
# =====================

    elif text=="2️⃣ 📈 Trading":

        send(chat,"Choose trading style",trading_menu)

    elif text=="1️⃣ Day Trading":

        send(chat,
"""
Day trading means opening and closing trades
within the same day to capture small price moves.
""",
        back_menu)

    elif text=="2️⃣ Swing Trading":

        send(chat,
"""
Swing trading holds positions for several days
or weeks to capture market trends.
""",
        back_menu)

    elif text=="3️⃣ Long-term Investing":

        send(chat,
"""
Long-term investors hold crypto for months
or years expecting future growth.
""",
        back_menu)


# =====================
# RISK
# =====================

    elif text=="3️⃣ ⚠ Risk":

        send(chat,
"""
Risk management is essential in trading.

• Never risk more than 2% per trade
• Always use stop-loss
• Avoid emotional trading
""",
        back_menu)


# =====================
# MARKET
# =====================

    elif text=="4️⃣ 📊 Market":

        send(chat,"Market cycles",market_menu)

    elif text=="1️⃣ Accumulation":

        send(chat,
"""
Accumulation phase occurs after a crash.

Smart investors slowly buy assets at low prices.
""",
        back_menu)

    elif text=="2️⃣ Uptrend":

        send(chat,
"""
Uptrend is when prices consistently rise
and market confidence returns.
""",
        back_menu)

    elif text=="3️⃣ Distribution":

        send(chat,
"""
Distribution is when early investors
start taking profits at high prices.
""",
        back_menu)

    elif text=="4️⃣ Downtrend":

        send(chat,
"""
Downtrend happens when selling pressure
pushes prices lower.
""",
        back_menu)


# =====================
# STAKING
# =====================

    elif text=="8️⃣ 🔒 Staking":

        send(chat,"Staking benefits",staking_menu)

    elif text=="1️⃣ Passive income":

        send(chat,
"""
Staking allows you to earn rewards
by locking your crypto to support a network.
""",
        back_menu)

    elif text=="2️⃣ Network security":

        send(chat,
"""
Staking validators help confirm transactions
and keep the blockchain secure.
""",
        back_menu)

    elif text=="3️⃣ Long-term strategy":

        send(chat,
"""
Staking encourages long-term holding
while generating passive rewards.
""",
        back_menu)


# =====================
# ALTCOINS
# =====================

    elif text=="7️⃣ 🌕 Altcoins":

        send(chat,
"""
Altcoins are cryptocurrencies other than Bitcoin.

Examples include Ethereum, Solana and Cardano.
""",
        back_menu)


# =====================
# PORTFOLIO
# =====================

    elif text=="9️⃣ 💼 Portfolio":

        send(chat,
"""
Example crypto portfolio:

50% Bitcoin
25% Ethereum
15% Altcoins
10% Stablecoins
""",
        back_menu)


# =====================
# PRICE
# =====================

    elif text=="5️⃣ 💰 Price":

        send(chat,"Choose coin",price_menu)

    elif text=="BTC":
        send(chat,f"BTC price: ${price('bitcoin')}")

    elif text=="ETH":
        send(chat,f"ETH price: ${price('ethereum')}")

    elif text=="SOL":
        send(chat,f"SOL price: ${price('solana')}")

    elif text=="BNB":
        send(chat,f"BNB price: ${price('binancecoin')}")


# =====================
# CHARTS (UNCHANGED)
# =====================

    elif text=="6️⃣ 📊 Charts":

        send(chat,"Choose chart",chart_menu)

    elif text=="BTC Chart":
        send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT")

    elif text=="ETH Chart":
        send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:ETHUSDT")

    elif text=="SOL Chart":
        send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:SOLUSDT")

    elif text=="BNB Chart":
        send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:BNBUSDT")


# =====================
# NEWS (UNCHANGED)
# =====================

    elif text=="🔟 📰 News":

        send(chat,crypto_news(),back_menu)


# =====================
# AI
# =====================

    elif text=="🧠 AI Assistant":

        ai_mode[chat]=True
        send(chat,"Ask any crypto question 🤖",back_menu)

    elif chat in ai_mode:

        answer=llama_ai(text)

        send(chat,answer,back_menu)


# =====================
# LANGUAGE
# =====================

    elif text=="🌍 Language":

        send(chat,"Choose language",language_menu)


# =====================
# BACK
# =====================

    elif text=="⬅ Back":

        ai_mode.pop(chat,None)

        send(chat,"Main menu",main_menu)

    return "ok"


# =====================
# SERVER START
# =====================

if __name__=="__main__":

    requests.get(URL+"deleteWebhook")

    WEBHOOK_URL=os.environ.get("RENDER_EXTERNAL_URL")+WEBHOOK_PATH

    requests.get(URL+"setWebhook",params={"url":WEBHOOK_URL})

    port=int(os.environ.get("PORT",10000))

    app.run(host="0.0.0.0",port=port)
