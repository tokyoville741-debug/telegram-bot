from flask import Flask, request
import requests
import os

app = Flask(__name__)

# ==============================
# CONFIG
# ==============================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


# ==============================
# SEND TELEGRAM MESSAGE
# ==============================

def send_message(chat_id, text, buttons=None):

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    if buttons:
        payload["reply_markup"] = {
            "keyboard": buttons,
            "resize_keyboard": True
        }

    try:
        requests.post(
            TELEGRAM_API,
            json=payload,
            timeout=10
        )
    except Exception as e:
        print("Telegram send error:", e)


# ==============================
# AI FUNCTION
# ==============================

def ask_ai(user_message):

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": """You are OpenClaw AI Coach.

You help users understand:
- cryptocurrency
- trading
- blockchain
- Binance ecosystem

Rules:
Always respond in English.
Be concise and educational.
Never give financial advice.
Encourage risk management.
"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "max_tokens": 400
    }

    response = requests.post(GROQ_URL, headers=headers, json=data, timeout=20)
    result = response.json()

    return result["choices"][0]["message"]["content"]


# ==============================
# HOME PAGE
# ==============================

@app.route("/")
def home():
    return "OpenClaw AI Coach is running 🚀"


# ==============================
# MAIN MENU
# ==============================

def main_menu(chat_id):

    text = """
🤖 OpenClaw AI Coach

Choose a section:

1️⃣ Learn
2️⃣ Trading
3️⃣ Risk
4️⃣ Market
5️⃣ Price
6️⃣ AI Analysis
7️⃣ Altcoins
8️⃣ Staking
9️⃣ Portfolio
🔟 News
"""

    buttons = [
        ["📚 Learn", "📈 Trading"],
        ["⚠️ Risk", "📊 Market"],
        ["💰 Price", "🧠 AI Analysis"],
        ["🪙 Altcoins", "🔒 Staking"],
        ["💼 Portfolio", "📰 News"]
    ]

    send_message(chat_id, text, buttons)


# ==============================
# TELEGRAM WEBHOOK
# ==============================

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    if "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")


    # ==========================
    # BACK BUTTON
    # ==========================

    if text == "🔙 Back":
        main_menu(chat_id)
        return "ok"


    # ==========================
    # BUTTON SHORTCUTS
    # ==========================

    if text == "📚 Learn":
        text = "/learn"

    elif text == "📈 Trading":
        text = "/trading"

    elif text == "⚠️ Risk":
        text = "/risk"

    elif text == "📊 Market":
        text = "/market"

    elif text == "💰 Price":
        text = "/prices"

    elif text == "🧠 AI Analysis":
        text = "/analyze BTC"

    elif text == "🪙 Altcoins":
        text = "/altcoins"

    elif text == "🔒 Staking":
        text = "/staking"

    elif text == "💼 Portfolio":
        text = "/portfolio"

    elif text == "📰 News":
        text = "/news"


    # ==========================
    # NUMBER SHORTCUTS
    # ==========================

    if text == "1":
        text = "/learn"
    elif text == "2":
        text = "/trading"
    elif text == "3":
        text = "/risk"
    elif text == "4":
        text = "/market"
    elif text == "5":
        text = "/prices"
    elif text == "6":
        text = "/analyze BTC"
    elif text == "7":
        text = "/altcoins"
    elif text == "8":
        text = "/staking"
    elif text == "9":
        text = "/portfolio"
    elif text == "10":
        text = "/news"


    # ==========================
    # COMMANDS
    # ==========================

    if text == "/start":
        main_menu(chat_id)
        return "ok"


    elif text == "/learn":

        reply = """
📚 Crypto Learning Hub

1️⃣ What is Blockchain
2️⃣ What is Bitcoin
3️⃣ What is Crypto Trading
4️⃣ Spot vs Futures
5️⃣ Risk Management
"""

        buttons = [["🔙 Back"]]
        send_message(chat_id, reply, buttons)
        return "ok"


    elif text == "/trading":

        reply = """
📈 Trading Basics

1️⃣ Support & Resistance
2️⃣ Market Trends
3️⃣ Moving Averages
4️⃣ RSI Indicator
5️⃣ Market Cycles
"""

        buttons = [["🔙 Back"]]
        send_message(chat_id, reply, buttons)
        return "ok"


    elif text == "/risk":

        reply = """
⚠️ Risk Management

1️⃣ Use stop losses
2️⃣ Manage position size
3️⃣ Control emotions
4️⃣ Diversify assets
"""

        buttons = [["🔙 Back"]]
        send_message(chat_id, reply, buttons)
        return "ok"


    elif text == "/market":

        reply = """
📊 Market Cycles

Bull market → optimism
Bear market → fear

Focus on:
trend + patience + discipline
"""

        buttons = [["🔙 Back"]]
        send_message(chat_id, reply, buttons)
        return "ok"


    elif text == "/portfolio":

        reply = """
💼 Portfolio Management

Diversify assets
Rebalance regularly

Example:

BTC 40%
ETH 30%
Alts 20%
Stablecoins 10%
"""

        buttons = [["🔙 Back"]]
        send_message(chat_id, reply, buttons)
        return "ok"


    elif text == "/prices":

        coins = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

        prices = []

        for coin in coins:
            try:
                url = f"https://api.binance.com/api/v3/ticker/price?symbol={coin}"
                r = requests.get(url)
                price = r.json()["price"]

                prices.append(f"{coin.replace('USDT','')} : ${float(price):,.2f}")

            except:
                prices.append(f"{coin} error")

        reply = "💰 Live Crypto Prices\n\n" + "\n".join(prices)

        buttons = [["🔙 Back"]]
        send_message(chat_id, reply, buttons)
        return "ok"


    elif text.startswith("/analyze"):

        coin = text.replace("/analyze", "").strip()

        if coin == "":
            coin = "BTC"

        reply = ask_ai(f"Give a short crypto market analysis for {coin}")

        buttons = [["🔙 Back"]]
        send_message(chat_id, reply, buttons)
        return "ok"


    elif text == "/news":

        reply = """
📰 Crypto News

1️⃣ CoinDesk
2️⃣ CoinTelegraph
3️⃣ Binance Research
"""

        buttons = [["🔙 Back"]]
        send_message(chat_id, reply, buttons)
        return "ok"


    elif text == "/altcoins":

        reply = """
🪙 Altcoin Guide

1️⃣ Ethereum
2️⃣ Solana
3️⃣ Cardano
4️⃣ Avalanche
"""

        buttons = [["🔙 Back"]]
        send_message(chat_id, reply, buttons)
        return "ok"


    elif text == "/staking":

        reply = """
🔒 Staking Guide

1️⃣ ETH
2️⃣ ADA
3️⃣ SOL
"""

        buttons = [["🔙 Back"]]
        send_message(chat_id, reply, buttons)
        return "ok"


    else:

        try:
            reply = ask_ai(text)

        except Exception as e:
            print("AI error:", e)
            reply = "AI error. Please try again."

        buttons = [["🔙 Back"]]
        send_message(chat_id, reply, buttons)

    return "ok"


# ==============================
# SERVER
# ==============================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)
