import requests
import time
import threading
import os
from flask import Flask

TOKEN = "TON_TOKEN_TELEGRAM"
LLAMA_API_KEY = "TA_CLE_LLAMA"

URL = f"https://api.telegram.org/bot{TOKEN}/"
LLAMA_URL = "https://api.llama-api.com/chat/completions"

app = Flask(__name__)

@app.route("/")
def home():
    return "Crypto bot running"


# MENUS

main_menu = {
    "keyboard":[
        ["📚 Learn","📈 Trading"],
        ["⚠ Risk","📊 Market"],
        ["💰 Price","📊 Charts"],
        ["🌕 Altcoins","🔒 Staking"],
        ["💼 Portfolio","📰 News"],
        ["🧠 AI Assistant"]
    ],
    "resize_keyboard":True
}

price_menu = {
    "keyboard":[
        ["BTC","ETH"],
        ["SOL","BNB"],
        ["⬅ Back"]
    ],
    "resize_keyboard":True
}

chart_menu = {
    "keyboard":[
        ["BTC Chart","ETH Chart"],
        ["SOL Chart","BNB Chart"],
        ["⬅ Back"]
    ],
    "resize_keyboard":True
}

back_menu = {
    "keyboard":[["⬅ Back"]],
    "resize_keyboard":True
}


# TELEGRAM SEND

def send(chat_id,text,keyboard=None):

    data = {
        "chat_id":chat_id,
        "text":text
    }

    if keyboard:
        data["reply_markup"]=keyboard

    try:
        requests.post(URL+"sendMessage",json=data,timeout=10)
    except:
        pass


# COIN PRICE

def price(coin):

    try:

        r = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd",
            timeout=10
        )

        data = r.json()

        return data.get(coin,{}).get("usd","Unavailable")

    except:

        return "Unavailable"


# CRYPTO NEWS

def crypto_news():

    try:

        r = requests.get(
            "https://min-api.cryptocompare.com/data/v2/news/?lang=EN",
            timeout=10
        )

        news = r.json().get("Data",[])[:5]

        text = "📰 Latest Crypto News\n\n"

        for n in news:

            text += f"{n['title']}\n{n['url']}\n\n"

        return text

    except:

        return "News unavailable."


# LLAMA AI

def llama_ai(question):

    headers = {
        "Authorization": f"Bearer {LLAMA_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama-3.3-70b-instruct",
        "messages": [
            {"role":"system","content":"You are a crypto trading assistant."},
            {"role":"user","content":question}
        ]
    }

    try:

        r = requests.post(
            LLAMA_URL,
            headers=headers,
            json=data,
            timeout=30
        )

        return r.json()["choices"][0]["message"]["content"]

    except:

        return "AI unavailable right now."


# TELEGRAM UPDATES

def updates(offset):

    try:

        r = requests.get(
            URL+"getUpdates",
            params={"offset":offset,"timeout":30},
            timeout=35
        )

        return r.json()

    except:

        return {}


# BOT LOOP

def bot():

    print("BOT STARTED")

    offset = 0

    while True:

        data = updates(offset)

        if "result" not in data:
            time.sleep(1)
            continue

        for u in data["result"]:

            offset = u["update_id"] + 1

            if "message" not in u:
                continue

            msg = u["message"]

            if "text" not in msg:
                continue

            chat = msg["chat"]["id"]
            text = msg["text"].strip()


            if text == "/start":

                send(chat,
                "🤖 Welcome to your Crypto AI Assistant\nChoose a menu:",
                main_menu)


            elif "Learn" in text:

                send(chat,
                "📚 Crypto Education\nCryptocurrency is digital money powered by blockchain.",
                back_menu)


            elif "Trading" in text:

                send(chat,
                "📈 Trading\nBuy and sell crypto to profit from price movements.",
                back_menu)


            elif "Risk" in text:

                send(chat,
                "⚠ Risk Management\nNever risk more than 2% per trade.",
                back_menu)


            elif "Market" in text:

                send(chat,
                "📊 Market Cycles\nAccumulation → Uptrend → Distribution → Downtrend",
                back_menu)


            elif "Price" in text:

                send(chat,"Choose a cryptocurrency:",price_menu)


            elif text == "BTC":

                send(chat,f"₿ Bitcoin price: ${price('bitcoin')}")


            elif text == "ETH":

                send(chat,f"Ξ Ethereum price: ${price('ethereum')}")


            elif text == "SOL":

                send(chat,f"◎ Solana price: ${price('solana')}")


            elif text == "BNB":

                send(chat,f"BNB price: ${price('binancecoin')}")


            elif "Charts" in text:

                send(chat,"Choose chart:",chart_menu)


            elif "BTC Chart" in text:

                send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT")


            elif "ETH Chart" in text:

                send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:ETHUSDT")


            elif "SOL Chart" in text:

                send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:SOLUSDT")


            elif "BNB Chart" in text:

                send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:BNBUSDT")


            elif "Altcoins" in text:

                send(chat,"🌕 Altcoins are cryptocurrencies other than Bitcoin.",back_menu)


            elif "Staking" in text:

                send(chat,"🔒 Staking lets you earn rewards by locking crypto.",back_menu)


            elif "Portfolio" in text:

                send(chat,"💼 Example Portfolio\n50% BTC\n25% ETH\n15% Altcoins\n10% Stablecoins",back_menu)


            elif "News" in text:

                send(chat,crypto_news(),back_menu)


            elif "AI" in text:

                send(chat,"Ask any crypto question.",back_menu)


            elif "Back" in text:

                send(chat,"Main menu",main_menu)


            else:

                reply = llama_ai(text)

                send(chat,reply)

        time.sleep(1)


# START

if __name__ == "__main__":

    threading.Thread(target=bot,daemon=True).start()

    port = int(os.environ.get("PORT",10000))

    app.run(host="0.0.0.0",port=port)
