from flask import Flask, request
import requests
import os

app = Flask(__name__)

# ==============================
# CONFIG
# ==============================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


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

You are an AI assistant designed to help users understand cryptocurrency,
trading, blockchain technology and the Binance ecosystem.

Your mission is to educate users clearly and simply.

Rules:
- Always respond in English
- Be concise and educational
- Help users understand trading concepts
- Explain Binance products when relevant
- Never give financial advice
- Encourage users to manage risk

Topics you help with:
Crypto education
Trading basics
Market psychology
Risk management
Binance platform tools
"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "max_tokens": 400
    }

    response = requests.post(GROQ_URL, headers=headers, json=data)

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

@app.route("/", methods=["POST"])
def webhook():

    data = request.get_json()

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

Available commands:

/learn - Start crypto lessons
/binance - Learn Binance features
/trading - Trading basics
/risk - Risk management
/market - Market insights

You can also ask any crypto question.
"""

    elif text == "/learn":

        reply = """
Crypto Learning Hub 📚

1️⃣ What is Blockchain
2️⃣ What is Bitcoin
3️⃣ What is Crypto Trading
4️⃣ Spot vs Futures
5️⃣ Risk Management

Ask me:
Explain blockchain
Explain Bitcoin
Explain futures trading
"""

    elif text == "/binance":

        reply = """
Binance Ecosystem Guide 🟡

Key Binance products:

• Spot Trading
Buy and sell cryptocurrencies instantly.

• Futures Trading
Trade crypto with leverage.

• Binance Earn
Earn passive income with your crypto.

• Binance Wallet
Secure storage for digital assets.

• Security
2FA, anti-phishing protection and asset safety.
"""

    elif text == "/trading":

        reply = """
Trading Basics 📈

Important concepts:

• Support and Resistance
• Trend analysis
• Moving averages
• RSI indicator
• Market cycles

Always remember:
Successful trading requires discipline and risk control.
"""

    elif text == "/risk":

        reply = """
Risk Management ⚠️

Golden rules of trading:

• Never risk more than you can afford to lose
• Use stop losses
• Avoid emotional trading
• Manage position size
• Diversify your portfolio

Risk management is the key to long-term survival.
"""

    elif text == "/market":

        reply = """
Market Insights 🔎

Crypto markets move in cycles:

• Bull markets
Prices rise and optimism grows.

• Bear markets
Prices fall and fear dominates.

Smart traders focus on:
trend, patience and risk control.

You can ask:
Is Bitcoin bullish?
What is a bull market?
"""

    else:

        try:
            reply = ask_ai(text)

        except Exception as e:
            reply = "AI error. Please try again."

    requests.post(TELEGRAM_API, json={
        "chat_id": chat_id,
        "text": reply
    })

    return "ok"


# ==============================
# SERVER
# ==============================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
