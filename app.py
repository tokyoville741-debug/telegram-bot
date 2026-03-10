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

risk_menu = [
["3.1 Risk Management"],
["3.2 Stop Loss"],
["3.3 Position Size"],
["⬅ Back"]
]

market_menu = [
["4.1 Bull Market"],
["4.2 Bear Market"],
["4.3 Market Cycle"],
["⬅ Back"]
]

altcoins_menu = [
["7.1 What are Altcoins"],
["7.2 Popular Altcoins"],
["7.3 Altcoin Season"],
["⬅ Back"]
]

staking_menu = [
["8.1 What is Staking"],
["8.2 Staking Rewards"],
["8.3 Proof of Stake"],
["⬅ Back"]
]

portfolio_menu = [
["9.1 Diversification"],
["9.2 Long Term Investing"],
["9.3 Portfolio Tracking"],
["9.4 Rebalancing"],
["⬅ Back"]
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
        "🚀 Welcome to OpenClaw AI Coach\n\n"

        "Your intelligent assistant for learning and exploring the world "
        "of cryptocurrency, trading, and blockchain technology.\n\n"

        "With OpenClaw AI Coach you can:\n"
        "📚 Learn crypto fundamentals\n"
        "📊 Understand trading strategies\n"
        "📉 Discover risk management techniques\n"
        "📈 Explore crypto charts\n"
        "🪙 Learn about altcoins\n"
        "💰 Understand staking and passive income\n"
        "📰 Stay updated with crypto news\n"
        "🤖 Ask the AI Assistant any question\n\n"

        "Whether you are a beginner or an experienced trader, "
        "this bot will help you understand the crypto ecosystem "
        "step by step.\n\n"

        "👇 Select a topic from the menu below.",
        main_menu)


# ================= BACK =================

    elif text == "⬅ Back":

        ai_mode[chat] = False

        send(chat,"Main Menu",main_menu)


# ================= LEARN =================

    elif text == "1 Learn":

        send(chat,
        "📚 Crypto Learning Section\n\n"
        "This section explains the most important concepts "
        "behind cryptocurrency and blockchain technology.",
        learn_menu)

    elif text == "1.1 What is Blockchain":

        send(chat,
        "📚 Blockchain\n\n"
        "Blockchain is a decentralized digital ledger that records "
        "transactions across many computers.\n\n"
        "Key features:\n"
        "• Decentralized\n"
        "• Transparent\n"
        "• Secure\n"
        "• Immutable\n\n"
        "It is the core technology behind cryptocurrencies.")

    elif text == "1.2 What is Bitcoin":

        send(chat,
        "₿ Bitcoin\n\n"
        "Bitcoin is the first cryptocurrency created in 2009 "
        "by an anonymous person known as Satoshi Nakamoto.\n\n"
        "It allows people to send digital money directly "
        "without banks or intermediaries.")

    elif text == "1.3 What is Ethereum":

        send(chat,
        "💎 Ethereum\n\n"
        "Ethereum is a blockchain platform that allows developers "
        "to build decentralized applications and smart contracts.\n\n"
        "It is the foundation of DeFi, NFTs and many crypto projects.")


# ================= TRADING =================

    elif text == "2 Trading":

        send(chat,
        "📊 Crypto Trading\n\n"
        "Learn how traders analyze markets and make trading decisions.",
        trading_menu)

    elif text == "2.1 Spot Trading":

        send(chat,
        "Spot trading means buying or selling cryptocurrency "
        "at the current market price.")

    elif text == "2.2 Futures Trading":

        send(chat,
        "Futures trading allows traders to speculate "
        "on price movements using leverage.")

    elif text == "2.3 Technical Analysis":

        send(chat,
        "Technical analysis studies charts, patterns and indicators "
        "to predict market movements.")


# ================= RISK =================

    elif text == "3 Risk":

        send(chat,
        "📉 Risk Management\n\n"
        "Professional traders focus more on protecting capital "
        "than chasing profits.",
        risk_menu)

    elif text == "3.1 Risk Management":

        send(chat,
        "Risk management is the discipline of controlling losses "
        "so that a few bad trades cannot destroy your portfolio.")

    elif text == "3.2 Stop Loss":

        send(chat,
        "A stop loss automatically closes a trade when price "
        "reaches a specific level to limit losses.")

    elif text == "3.3 Position Size":

        send(chat,
        "Position sizing determines how much capital "
        "you allocate to a single trade.")


# ================= MARKET =================

    elif text == "4 Market":

        send(chat,
        "📊 Crypto Market Cycles\n\n"
        "Understanding market conditions is essential.",
        market_menu)

    elif text == "4.1 Bull Market":

        send(chat,
        "A bull market is a period where crypto prices "
        "increase for a long time.")

    elif text == "4.2 Bear Market":

        send(chat,
        "A bear market is when prices decline "
        "and investor confidence falls.")

    elif text == "4.3 Market Cycle":

        send(chat,
        "Markets move through cycles:\n"
        "Accumulation → Bull Market → Distribution → Bear Market.")


# ================= ALTS =================

    elif text == "7 Altcoins":

        send(chat,
        "🪙 Altcoins\n\n"
        "Altcoins are cryptocurrencies other than Bitcoin.",
        altcoins_menu)

    elif text == "7.1 What are Altcoins":

        send(chat,
        "Altcoins are alternative cryptocurrencies created "
        "after Bitcoin.")

    elif text == "7.2 Popular Altcoins":

        send(chat,
        "Popular altcoins include:\n"
        "Ethereum\nBNB\nSolana\nCardano")

    elif text == "7.3 Altcoin Season":

        send(chat,
        "Altcoin season occurs when altcoins "
        "outperform Bitcoin.")


# ================= STAKING =================

    elif text == "8 Staking":

        send(chat,
        "💰 Staking\n\n"
        "Earn passive rewards by locking crypto.",
        staking_menu)

    elif text == "8.1 What is Staking":

        send(chat,
        "Staking allows users to lock cryptocurrency "
        "to support blockchain networks.")

    elif text == "8.2 Staking Rewards":

        send(chat,
        "Staking rewards are payments given to users "
        "who help secure the network.")

    elif text == "8.3 Proof of Stake":

        send(chat,
        "Proof of Stake is a consensus mechanism "
        "used by many modern blockchains.")


# ================= CHARTS =================

    elif text == "6 Charts":

        send(chat,"Open crypto charts.",charts_menu)

    elif text == "6.1 BTC Chart":

        send(chat,"https://www.tradingview.com/symbols/BTCUSDT/")

    elif text == "6.2 ETH Chart":

        send(chat,"https://www.tradingview.com/symbols/ETHUSDT/")

    elif text == "6.3 BNB Chart":

        send(chat,"https://www.tradingview.com/symbols/BNBUSDT/")

    elif text == "6.4 SOL Chart":

        send(chat,"https://www.tradingview.com/symbols/SOLUSDT/")


# ================= NEWS =================

    elif text=="10 News":

        send(chat,"Crypto news sources.",news_menu)

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

        send(chat,"Ask any crypto question. Press Back to exit.")

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

        send(chat,"Choose language.",language_menu)

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
