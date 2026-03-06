from flask import Flask, request
import requests
import os

app = Flask(__name__)

# ==============================
# CONFIG
# ==============================

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# ==============================
# PAGE TEST
# ==============================

@app.route("/")
def home():
    return "OpenClaw AI Coach Bot is running 🚀"

# ==============================
# TELEGRAM WEBHOOK
# ==============================

@app.route("/", methods=["POST"])
def webhook():

    data = request.get_json()

    if "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    user_message = data["message"].get("text", "")

    if not user_message:
        return "ok"

    # ==============================
    # COMMANDS
    # ==============================

    if user_message == "/start":

        reply = """Welcome to OpenClaw AI Coach 🚀

Your AI assistant for crypto and trading.

I can help you with:

• Crypto education
• Trading basics
• Blockchain concepts
• Binance ecosystem
• Market tips

Commands:
/learn - Learn crypto basics
/trading - Learn trading
/tips - Trading tips

Or ask any crypto question!"""

    elif user_message == "/learn":

        reply = """Crypto Basics 📚

1. Blockchain = decentralized digital ledger
2. Bitcoin = first cryptocurrency
3. Altcoins = other cryptocurrencies
4. Wallet = store your crypto safely
5. Exchange = platform to trade crypto

Example exchanges:
• Binance
• Coinbase
• Kraken

Crypto is transforming finance worldwide."""

    elif user_message == "/trading":

        reply = """Crypto Trading Basics 📊

Types of trading:

• Spot Trading
Buy and sell crypto instantly.

• Futures Trading
Trade with leverage.

Important concepts:

• Support
• Resistance
• Stop Loss
• Take Profit
• Risk Management

Trade smart and manage risk."""

    elif user_message == "/tips":

        reply = """Trading Tips 💡

1. Never invest more than you can afford to lose
2. Always use stop-loss
3. Avoid emotional trading
4. Follow market trends
5. Diversify your portfolio

Success in trading requires patience and discipline."""

    else:

        # ==============================
        # AI RESPONSE (LLAMA 3)
        # ==============================

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a crypto and trading assistant helping users understand blockchain, crypto and trading concepts."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "max_tokens": 500
        }

        try:

            response = requests.post(GROQ_URL, headers=headers, json=payload)
            result = response.json()

            reply = result["choices"][0]["message"]["content"]

        except Exception as e:

            reply = "AI error: " + str(e)

    # ==============================
    # SEND MESSAGE TO TELEGRAM
    # ==============================

    requests.post(TELEGRAM_API, json={
        "chat_id": chat_id,
        "text": reply
    })

    return "ok"

# ==============================
# RUN SERVER
# ==============================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
