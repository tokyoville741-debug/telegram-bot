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


languages={}

language_menu={
"keyboard":[
["🇬🇧 English","🇫🇷 Français"],
["🇪🇸 Español"],
["⬅ Back"]
],
"resize_keyboard":True
}

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

back_menu={
"keyboard":[["⬅ Back"]],
"resize_keyboard":True
}


def send(chat_id,text,keyboard=None):

    payload={"chat_id":chat_id,"text":text}

    if keyboard:
        payload["reply_markup"]=keyboard

    requests.post(URL+"sendMessage",json=payload)


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


def llama_ai(question):

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

    r=requests.post(LLAMA_URL,headers=headers,json=data)

    result=r.json()

    return result["choices"][0]["message"]["content"]


def get_updates(offset):

    r=requests.get(URL+"getUpdates",params={"offset":offset,"timeout":25})

    return r.json()


def run_bot():

    offset=None
    ai_mode={}

    while True:

        data=get_updates(offset)

        if "result" not in data:
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
            text=msg["text"]


            if text=="/start":

                send(chat,
"""
🤖 Welcome to the Crypto AI Assistant

This bot helps you learn cryptocurrency step by step.
""",
                main_menu)


            elif text=="1️⃣ 📚 Learn":

                send(chat,
"""
📚 Cryptocurrency is digital money powered by blockchain technology.
""",
                back_menu)


            elif text=="3️⃣ ⚠ Risk":

                send(chat,
"""
⚠ Risk management is essential in trading.

Never risk more than 2% per trade.
Always use stop-loss.
Avoid emotional trading.
""",
                back_menu)


            elif text=="7️⃣ 🌕 Altcoins":

                send(chat,
"""
🌕 Altcoins are cryptocurrencies other than Bitcoin.

Examples include Ethereum, Solana, Cardano.
""",
                back_menu)


            elif text=="9️⃣ 💼 Portfolio":

                send(chat,
"""
💼 Example portfolio:

50% Bitcoin
25% Ethereum
15% Altcoins
10% Stablecoins
""",
                back_menu)


            elif text=="🔟 📰 News":

                send(chat,crypto_news(),back_menu)


            elif text=="🧠 AI Assistant":

                ai_mode[chat]=True
                send(chat,"Ask any crypto question 🤖",back_menu)


            elif chat in ai_mode:

                answer=llama_ai(text)

                send(chat,answer,back_menu)


            elif text=="🌍 Language":

                send(chat,"Choose language",language_menu)


            elif text=="🇬🇧 English":
                send(chat,"Language set to English",main_menu)

            elif text=="🇫🇷 Français":
                send(chat,"Langue définie sur Français",main_menu)

            elif text=="🇪🇸 Español":
                send(chat,"Idioma configurado",main_menu)


            elif text=="2️⃣ 📈 Trading":

                send(chat,"Choose trading style",trading_menu)


            elif text=="4️⃣ 📊 Market":

                send(chat,"Market cycles",market_menu)


            elif text=="8️⃣ 🔒 Staking":

                send(chat,"Staking benefits",staking_menu)


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


            elif text=="⬅ Back":

                ai_mode.pop(chat,None)

                send(chat,"Main menu",main_menu)


        time.sleep(1)


if __name__=="__main__":

    threading.Thread(target=run_bot).start()

    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
