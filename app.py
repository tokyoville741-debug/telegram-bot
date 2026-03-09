import os
import requests
import time
import threading
from flask import Flask

app = Flask(__name__)

# =========================
# BOT CONFIG
# =========================

TOKEN = os.environ.get("BOT_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/"

ai_mode = {}
languages = {}

# =========================
# WEB SERVER
# =========================

@app.route("/")
def home():
    return "Crypto AI Bot running 🚀"

# =========================
# MENUS
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

back_menu={
"keyboard":[["⬅ Back"]],
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

price_menu={
"keyboard":[
["BTC","ETH"],
["BNB","SOL"],
["⬅ Back"]
],
"resize_keyboard":True
}

chart_menu={
"keyboard":[
["BTC Chart","ETH Chart"],
["BNB Chart","SOL Chart"],
["⬅ Back"]
],
"resize_keyboard":True
}

trading_menu={
"keyboard":[
["1️⃣ Day Trading"],
["2️⃣ Swing Trading"],
["3️⃣ Scalping"],
["4️⃣ Long-term Investing"],
["⬅ Back"]
],
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
        requests.post(URL+"sendMessage",json=payload)
    except:
        pass

# =========================
# GET UPDATES
# =========================

def get_updates(offset):

    try:

        r=requests.get(
            URL+"getUpdates",
            params={"offset":offset,"timeout":25}
        )

        return r.json()

    except:

        return {}

# =========================
# CRYPTO PRICE
# =========================

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

# =========================
# NEWS
# =========================

def crypto_news():

    return """
📰 CRYPTO NEWS

Bitcoin adoption continues growing globally.

Ethereum ecosystem expands through DeFi and NFTs.

Institutional investors are entering crypto markets.

Always research before investing.
"""

# =========================
# AI ASSISTANT
# =========================

def llama_ai(question):

    return "🤖 AI: Crypto markets are volatile. Always manage risk and diversify."

# =========================
# BOT LOOP
# =========================

def run_bot():

    offset=0

    while True:

        updates=get_updates(offset)

        if "result" in updates:

            for update in updates["result"]:

                offset=update["update_id"]+1

                if "message" not in update:
                    continue

                msg=update["message"]
                chat=msg["chat"]["id"]
                text=msg.get("text","")

                text=text.strip()

                # START
                if text=="/start":

                    welcome="""
🤖 Welcome to the Crypto AI Bot

Learn crypto step by step.

1️⃣ Learn
2️⃣ Trading
3️⃣ Risk
4️⃣ Market
5️⃣ Price
6️⃣ Charts
7️⃣ Altcoins
8️⃣ Staking
9️⃣ Portfolio
🔟 News
🧠 AI Assistant
"""

                    send(chat,welcome,main_menu)

                # LANGUAGE
                elif text=="🌍 Language":
                    send(chat,"Choose language:",language_menu)

                elif text=="🇬🇧 English":
                    languages[chat]="en"
                    send(chat,"Language set to English",main_menu)

                elif text=="🇫🇷 Français":
                    languages[chat]="fr"
                    send(chat,"Langue définie sur Français",main_menu)

                elif text=="🇪🇸 Español":
                    languages[chat]="es"
                    send(chat,"Idioma configurado",main_menu)

                # LEARN
                elif text=="1️⃣ 📚 Learn":

                    send(chat,
"""
📚 WHAT IS CRYPTO?

Cryptocurrency is digital money secured by blockchain technology.

Advantages:
• decentralized
• transparent
• global
• secure
""",
                    back_menu)

                # TRADING
                elif text=="2️⃣ 📈 Trading":
                    send(chat,"Trading education:",trading_menu)

                elif text=="1️⃣ Day Trading":

                    send(chat,
"""
📈 DAY TRADING

Buying and selling within the same day.
""",
                    back_menu)

                elif text=="2️⃣ Swing Trading":

                    send(chat,
"""
📊 SWING TRADING

Holding trades for days or weeks.
""",
                    back_menu)

                elif text=="3️⃣ Scalping":

                    send(chat,
"""
⚡ SCALPING

Very short trades lasting seconds.
""",
                    back_menu)

                elif text=="4️⃣ Long-term Investing":

                    send(chat,
"""
🪙 LONG TERM INVESTING

Holding crypto for months or years.
""",
                    back_menu)

                # RISK
                elif text=="3️⃣ ⚠ Risk":

                    send(chat,
"""
⚠ RISK MANAGEMENT

Never risk more than 2% per trade.
Use stop-loss orders.
""",
                    back_menu)

                # MARKET
                elif text=="4️⃣ 📊 Market":

                    send(chat,
"""
📊 MARKET CYCLES

Accumulation
Uptrend
Distribution
Downtrend
""",
                    back_menu)

                # PRICE
                elif text=="5️⃣ 💰 Price":
                    send(chat,"Choose coin:",price_menu)

                elif text=="BTC":
                    send(chat,f"Bitcoin: ${price('bitcoin')}")

                elif text=="ETH":
                    send(chat,f"Ethereum: ${price('ethereum')}")

                elif text=="BNB":
                    send(chat,f"BNB: ${price('binancecoin')}")

                elif text=="SOL":
                    send(chat,f"Solana: ${price('solana')}")

                # CHARTS
                elif text=="6️⃣ 📊 Charts":
                    send(chat,"Choose chart:",chart_menu)

                elif text=="BTC Chart":
                    send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT")

                elif text=="ETH Chart":
                    send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:ETHUSDT")

                # ALTCOINS
                elif text=="7️⃣ 🌕 Altcoins":

                    send(chat,
"""
Altcoins = cryptocurrencies other than Bitcoin.

Examples:
Ethereum
Solana
Cardano
""",
                    back_menu)

                # STAKING
                elif text=="8️⃣ 🔒 Staking":

                    send(chat,
"""
Staking allows earning rewards by locking crypto.
""",
                    back_menu)

                # PORTFOLIO
                elif text=="9️⃣ 💼 Portfolio":

                    send(chat,
"""
Example portfolio:

50% Bitcoin
25% Ethereum
15% Altcoins
10% Stablecoins
""",
                    back_menu)

                # NEWS
                elif text=="🔟 📰 News":
                    send(chat,crypto_news(),back_menu)

                # AI
                elif text=="🧠 AI Assistant":

                    ai_mode[chat]=True
                    send(chat,"Ask a crypto question.",back_menu)

                elif text=="⬅ Back":

                    ai_mode.pop(chat,None)
                    send(chat,"Main menu",main_menu)

                else:

                    if ai_mode.get(chat):

                        reply=llama_ai(text)
                        send(chat,reply)

                    else:

                        send(chat,"Choose an option.",main_menu)

        time.sleep(1)

# =========================
# START BOT
# =========================

if __name__=="__main__":

    bot_thread=threading.Thread(target=run_bot)
    bot_thread.start()

    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
