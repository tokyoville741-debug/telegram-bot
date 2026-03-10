import os
import requests
import threading
import time
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

ai_mode = {}

webhook_set = False


# ================= SEND MESSAGE =================
def send(chat, text, keyboard=None):

    data = {
        "chat_id": chat,
        "text": text
    }

    if keyboard:
        data["reply_markup"] = {
            "keyboard": keyboard,
            "resize_keyboard": True
        }

    requests.post(URL + "/sendMessage", json=data)


# ================= MENUS =================

main_menu = [
["1 Learn","2 Trading"],
["3 Risk","4 Market"],
["5 Price","6 Charts"],
["7 Altcoins","8 Staking"],
["9 Portfolio","10 News"],
["11 AI Assistant"],
["Language"]
]

charts_menu = [
["6.1 BTC Chart","6.2 ETH Chart"],
["6.3 BNB Chart","6.4 SOL Chart"],
["⬅ Back"]
]

news_menu = [
["10.1 CoinDesk"],
["10.2 CoinTelegraph"],
["10.3 Decrypt"],
["10.4 Binance News"],
["⬅ Back"]
]

learn_menu = [
["1.1 What is Blockchain"],
["1.2 What is Bitcoin"],
["1.3 What is Ethereum"],
["⬅ Back"]
]

trading_menu = [
["2.1 Spot Trading"],
["2.2 Futures Trading"],
["2.3 Technical Analysis"],
["⬅ Back"]
]

portfolio_menu = [
["9.1 Diversification"],
["9.2 Long Term Investing"],
["9.3 Portfolio Tracking"],
["9.4 Rebalancing"],
["⬅ Back"]
]

language_menu = [
["English"],
["Français"],
["Español"],
["⬅ Back"]
]


# ================= WEBHOOK =================

@app.route(f"/{TOKEN}", methods=["POST"])
def bot():

    data = request.get_json()

    if "message" not in data:
        return "ok"

    chat = data["message"]["chat"]["id"]
    text = data["message"].get("text","")

    # ================= START =================

    if text == "/start":

        ai_mode[chat] = False

        send(chat,
        "Welcome to OpenClaw AI Coach.\n\n"
        "Select a topic from the menu.",
        main_menu)


    # ================= BACK =================

    elif text == "⬅ Back":

        ai_mode[chat] = False

        send(chat,"Main Menu",main_menu)


    # ================= LEARN =================

    elif text == "1 Learn":

        send(chat,
        "1 Learn\n\n"
        "This section explains crypto basics.",
        learn_menu)

    elif text == "1.1 What is Blockchain":

        send(chat,
        "Blockchain is a decentralized ledger "
        "used to record transactions.")

    elif text == "1.2 What is Bitcoin":

        send(chat,
        "Bitcoin is the first cryptocurrency "
        "created in 2009.")

    elif text == "1.3 What is Ethereum":

        send(chat,
        "Ethereum is a blockchain that allows "
        "smart contracts.")


    # ================= TRADING =================

    elif text == "2 Trading":

        send(chat,
        "2 Trading\n\n"
        "Learn trading strategies.",
        trading_menu)

    elif text == "2.1 Spot Trading":

        send(chat,
        "Spot trading means buying crypto "
        "at current market price.")

    elif text == "2.2 Futures Trading":

        send(chat,
        "Futures trading allows leveraged positions.")

    elif text == "2.3 Technical Analysis":

        send(chat,
        "Technical analysis studies charts "
        "to predict price movement.")


    # ================= CHARTS =================

    elif text == "6 Charts":

        send(chat,
        "6 Charts\n\n"
        "Open charts on TradingView.",
        charts_menu)

    elif text == "6.1 BTC Chart":

        send(chat,"https://www.tradingview.com/symbols/BTCUSDT/")

    elif text == "6.2 ETH Chart":

        send(chat,"https://www.tradingview.com/symbols/ETHUSDT/")

    elif text == "6.3 BNB Chart":

        send(chat,"https://www.tradingview.com/symbols/BNBUSDT/")

    elif text == "6.4 SOL Chart":

        send(chat,"https://www.tradingview.com/symbols/SOLUSDT/")


    # ================= PORTFOLIO =================

    elif text == "9 Portfolio":

        send(chat,
        "9 Portfolio Management\n\n"
        "Managing a portfolio involves tracking "
        "different assets.",
        portfolio_menu)

    elif text=="9.1 Diversification":

        send(chat,"Diversification spreads assets.")

    elif text=="9.2 Long Term Investing":

        send(chat,"Long term investing focuses on growth.")

    elif text=="9.3 Portfolio Tracking":

        send(chat,"Tracking helps measure performance.")

    elif text=="9.4 Rebalancing":

        send(chat,"Rebalancing adjusts allocations.")


    # ================= NEWS =================

    elif text=="10 News":

        send(chat,
        "10 Crypto News Sources\n\n"
        "Select a news source.",
        news_menu)

    elif text=="10.1 CoinDesk":

        send(chat,"https://www.coindesk.com")

    elif text=="10.2 CoinTelegraph":

        send(chat,"https://cointelegraph.com")

    elif text=="10.3 Decrypt":

        send(chat,"https://decrypt.co")

    elif text=="10.4 Binance News":

        send(chat,"https://www.binance.com/en/news")


    # ================= AI =================

    elif text == "11 AI Assistant":

        ai_mode[chat] = True

        send(chat,
        "AI Assistant\n\n"
        "Ask any crypto question.\n\n"
        "Press Back to exit.")


    elif chat in ai_mode and ai_mode[chat]:

        try:

            r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type":"application/json"
            },
            json={
            "model":"llama-3.3-70b-versatile",
            "messages":[
            {"role":"system","content":"You are a crypto expert assistant."},
            {"role":"user","content":text}
            ]
            })

            answer = r.json()["choices"][0]["message"]["content"]

            send(chat,answer)

        except:

            send(chat,"AI service unavailable.")


    # ================= LANGUAGE =================

    elif text == "Language":

        send(chat,
        "Choose your preferred language.",
        language_menu)

    elif text == "Français":

        send(chat,"Langue changée en Français.")

    elif text == "Español":

        send(chat,"Idioma cambiado a Español.")

    elif text == "English":

        send(chat,"Language set to English.")

    return "ok"


# ================= WEBHOOK SETUP =================

@app.before_request
def setup_webhook():

    global webhook_set

    if not webhook_set:

        url = os.environ.get("RENDER_EXTERNAL_URL") + f"/{TOKEN}"

        requests.get(URL + "/setWebhook", params={"url":url})

        webhook_set = True


# ================= ANTI SLEEP =================

def keep_alive():

    while True:

        try:

            requests.get(os.environ.get("RENDER_EXTERNAL_URL"))

        except:
            pass

        time.sleep(300)


threading.Thread(target=keep_alive).start()


# ================= RUN =================

if __name__ == "__main__":

    port = int(os.environ.get("PORT",10000))

    app.run(host="0.0.0.0", port=port)
