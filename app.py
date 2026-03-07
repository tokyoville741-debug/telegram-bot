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

def send_message(chat_id, text):
    try:
        requests.post(
            TELEGRAM_API,
            json={
                "chat_id": chat_id,
                "text": text
            },
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
# TELEGRAM WEBHOOK
# ==============================

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    print(data)

    if "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    # ==========================
    # COMMANDS
    # ==========================

    if text == "/start":

        reply = """
Welcome to OpenClaw AI Coach 🚀

Your AI assistant for learning crypto and mastering the Binance ecosystem.

Commands:

/learn
/binance
/trading
/risk
/market
/portfolio
"""

    elif text == "/learn":

        reply = """
Crypto Learning Hub 📚

Topics:

• What is Blockchain
• What is Bitcoin
• What is Crypto Trading
• Spot vs Futures
• Risk Management
"""

    elif text == "/binance":

        reply = """
Binance Ecosystem Guide 🟡

• Spot Trading
• Futures Trading
• Binance Earn
• Binance Wallet
• Security Tools
"""

    elif text == "/trading":

        reply = """
Trading Basics 📈

Key concepts:

• Support & Resistance
• Trends
• Moving averages
• RSI indicator
• Market cycles
"""

    elif text == "/risk":

        reply = """
Risk Management ⚠️

Golden rules:

• Use stop losses
• Manage position size
• Control emotions
• Diversify assets
"""

    elif text == "/market":

        reply = """
Market Cycles 🔎

Bull market → optimism

Bear market → fear

Successful traders focus on:
trend + patience + discipline
"""

    elif text == "/portfolio":

        reply = """
Portfolio Management 💼

Basic strategy:

• Diversify assets
• Allocate capital wisely
• Avoid overexposure
• Rebalance regularly

Example:

BTC 40%
ETH 30%
Alts 20%
Stablecoins 10%
"""

    else:

        try:
            reply = ask_ai(text)

        except Exception as e:
            print("AI error:", e)
            reply = "AI error. Please try again."

    send_message(chat_id, reply)

    return "ok"


# ==============================
# SERVER
# ==============================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)
