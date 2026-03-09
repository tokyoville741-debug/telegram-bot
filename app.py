import requests
import time
import os
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

        return data.get(coin,{}).get("usd","Unavailable")

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


# LLAMA AI

def llama_ai(question):

    headers = {
        "Authorization": f"Bearer {LLAMA_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model":"meta-llama-3.3-70b-instruct",
        "messages":[
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

        result = r.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:

        print("LLAMA ERROR:",e)

        return "AI unavailable."


# TELEGRAM UPDATES

def get_updates(offset):

    try:

        r = requests.get(
            URL+"getUpdates",
            params={"offset":offset,"timeout":25},
            timeout=30
        )

        return r.json()

    except Exception as e:

        print("Update error:",e)
        return {}


# BOT LOOP

def run_bot():

    print("Bot started")

    offset = None

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

                send(chat,
                "🤖 Welcome to your Crypto AI Assistant",
                main_menu)


            elif "Learn" in text:

                send(chat,
                "📚 Cryptocurrency is digital money powered by blockchain.",
                back_menu)


            elif "Trading" in text:

                send(chat,
                "📈 Trading means buying and selling crypto to profit.",
                back_menu)


            elif "Risk" in text:

                send(chat,
                "⚠ Never risk more than 2% of capital per trade.",
                back_menu)


            elif "Market" in text:

                send(chat,
                "📊 Market cycles: Accumulation → Uptrend → Distribution → Downtrend",
                back_menu)


            elif "Price" in text:

                send(chat,"Choose a coin:",price_menu)


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

                send(chat,"🔒 Staking allows earning rewards by locking crypto.",back_menu)


            elif "Portfolio" in text:

                send(chat,"💼 Example Portfolio\n50% BTC\n25% ETH\n15% Altcoins\n10% Stablecoins",back_menu)


            elif "News" in text:

                send(chat,crypto_news(),back_menu)


            elif "Back" in text:

                send(chat,"Main menu",main_menu)


            else:

                reply = llama_ai(text)

                send(chat,reply)

        time.sleep(1)


# START BOT

if __name__ == "__main__":

    run_bot()
