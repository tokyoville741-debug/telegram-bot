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


# SEND MESSAGE

def send(chat_id,text,keyboard=None):

    payload = {
        "chat_id":chat_id,
        "text":text
    }

    if keyboard:
        payload["reply_markup"] = keyboard

    try:
        requests.post(URL+"sendMessage",json=payload,timeout=10)
    except Exception as e:
        print("Send error:",e)


# CRYPTO PRICE

def price(coin):

    try:

        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids":coin,"vs_currencies":"usd"},
            timeout=10
        )

        data = r.json()

        if coin in data:
            return data[coin]["usd"]

        return "Unavailable"

    except:
        return "Unavailable"


# NEWS

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


# AI

def llama_ai(question):

    if not LLAMA_API_KEY:
        return "AI unavailable."

    headers = {
        "Authorization": f"Bearer {LLAMA_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model":"meta-llama-3.3-70b-instruct",
        "messages":[
            {"role":"system","content":"You are a crypto assistant."},
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

        result = r.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"]

        return "AI unavailable."

    except:
        return "AI unavailable."


# TELEGRAM

def get_updates(offset):

    try:

        r = requests.get(
            URL+"getUpdates",
            params={"offset":offset,"timeout":25},
            timeout=30
        )

        return r.json()

    except:
        return {}


# BOT LOOP

def run_bot():

    offset = None
    ai_mode = {}

    while True:

        data = get_updates(offset)

        if not data or "result" not in data:
            time.sleep(2)
            continue

        for update in data["result"]:

            offset = update["update_id"] + 1

            if "message" not in update:
                continue

            msg = update["message"]

            if "text" not in msg:
                continue

            chat = msg["chat"]["id"]
            text = msg["text"].strip()


            if text == "/start":

                send(chat,"🤖 Welcome to your Crypto AI Assistant",main_menu)


            elif text == "📚 Learn":

                send(chat,
                "📚 Cryptocurrency is digital money powered by blockchain.",
                back_menu)


            elif text == "📈 Trading":

                send(chat,
                "📈 Trading means buying and selling crypto to profit.",
                back_menu)


            elif text == "⚠ Risk":

                send(chat,
                "⚠ Never risk more than 2% of capital per trade.",
                back_menu)


            elif text == "📊 Market":

                send(chat,
                "📊 Market cycles: Accumulation → Uptrend → Distribution → Downtrend",
                back_menu)


            elif text == "💰 Price":

                send(chat,"Choose a coin:",price_menu)


            elif text == "BTC":

                send(chat,f"₿ Bitcoin price: ${price('bitcoin')}")


            elif text == "ETH":

                send(chat,f"Ξ Ethereum price: ${price('ethereum')}")


            elif text == "SOL":

                send(chat,f"◎ Solana price: ${price('solana')}")


            elif text == "BNB":

                send(chat,f"BNB price: ${price('binancecoin')}")


            elif text == "📊 Charts":

                send(chat,"Choose chart:",chart_menu)


            elif text == "BTC Chart":

                send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT")


            elif text == "ETH Chart":

                send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:ETHUSDT")


            elif text == "SOL Chart":

                send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:SOLUSDT")


            elif text == "BNB Chart":

                send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:BNBUSDT")


            elif text == "🌕 Altcoins":

                send(chat,"🌕 Altcoins are cryptocurrencies other than Bitcoin.",back_menu)


            elif text == "🔒 Staking":

                send(chat,
                "🔒 Staking allows earning rewards by locking crypto in a network.",
                back_menu)


            elif text == "💼 Portfolio":

                send(chat,
                "💼 Example Portfolio\n50% BTC\n25% ETH\n15% Altcoins\n10% Stablecoins",
                back_menu)


            elif text == "📰 News":

                send(chat,crypto_news(),back_menu)


            elif text == "🧠 AI Assistant":

                ai_mode[chat] = True
                send(chat,"Ask any crypto question.",back_menu)


            elif text == "⬅ Back":

                ai_mode[chat] = False
                send(chat,"Main menu",main_menu)


            else:

                if ai_mode.get(chat):
                    reply = llama_ai(text)
                    send(chat,reply)
                else:
                    send(chat,"Choose an option.",main_menu)

        time.sleep(1)


# START BOT

if __name__ == "__main__":

    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    port = int(os.environ.get("PORT",10000))

    app.run(host="0.0.0.0",port=port)
