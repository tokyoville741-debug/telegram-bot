from flask import Flask, request
import requests
import os
from groq import Groq

app = Flask(__name__)

# ==============================
# CONFIGURATION
# ==============================

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# ==============================
# PAGE TEST
# ==============================

@app.route("/")
def home():
    return "OpenClaw AI Coach Bot is running 🚀"


# ==============================
# CRYPTO PRICE FUNCTION
# ==============================

def get_crypto_price(symbol):

    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        response = requests.get(url).json()

        price = response["price"]

        return f"{symbol} price: ${price}"

    except:
        return "Unable to fetch price."


# ==============================
# DCA SIMULATOR
# ==============================

def dca_simulation():

    text = """
DCA Strategy Example 📈

Invest $100 every month in Bitcoin.

After 12 months:

Total invested: $1200

Advantages:
• Reduces volatility risk
• No need to time the market
• Long-term accumulation strategy

This is one of the most used strategies by crypto investors.
"""

    return text


# ==============================
# AI ANALYSIS
# ==============================

def ai_response(message):

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a crypto AI coach helping users understand Binance ecosystem, trading, and crypto markets."
            },
            {
                "role": "user",
                "content": message
            }
        ],
        max_tokens=500
    )

    return completion.choices[0].message.content


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

    reply = ""

    # ==============================
    # COMMANDS
    # ==============================

    if user_message == "/start":

        reply = """
Welcome to OpenClaw AI Coach 🚀

Your AI assistant for learning crypto and mastering the Binance ecosystem.

Commands:

/learn - Crypto learning hub
/trading - Trading basics
/risk - Risk management
/market - Market insights
/price BTC - Check crypto price
/signal BTC - AI trading analysis
/dca - Investment simulator

You can also ask any crypto question.
"""

    elif user_message == "/learn":

        reply = """
Crypto Learning Hub 📚

1 What is Blockchain
2 What is Bitcoin
3 What is Crypto Trading
4 Spot vs Futures
5 Risk Management

Ask:
Explain blockchain
Explain bitcoin
Explain futures trading
"""

    elif user_message == "/trading":

        reply = """
Trading Basics 📊

Important concepts:

• Support and Resistance
• Market Trends
• Technical Indicators
• Volume analysis

Always trade with a plan and risk management.
"""

    elif user_message == "/risk":

        reply = """
Risk Management ⚠️

Golden rules:

• Never risk more than 2% per trade
• Always use stop-loss
• Avoid emotional trading
• Diversify your portfolio
"""

    elif user_message == "/market":

        reply = """
Market Insights 🔎

Crypto markets move in cycles:

Bull Market:
Prices rise and optimism grows.

Bear Market:
Prices fall and fear dominates.

Smart traders focus on trend and patience.
"""

    elif user_message.startswith("/price"):

        try:
            symbol = user_message.split(" ")[1].upper()
            reply = get_crypto_price(symbol)
        except:
            reply = "Example: /price BTC"

    elif user_message.startswith("/signal"):

        try:
            symbol = user_message.split(" ")[1].upper()

            analysis_prompt = f"""
Give a short crypto trading analysis for {symbol}.
Include trend, momentum and risk level.
"""

            reply = ai_response(analysis_prompt)

        except:
            reply = "Example: /signal BTC"

    elif user_message == "/dca":

        reply = dca_simulation()

    else:

        try:
            reply = ai_response(user_message)

        except Exception as e:

            reply = "AI error: " + str(e)

    # SEND MESSAGE

    requests.post(TELEGRAM_API, json={
        "chat_id": chat_id,
        "text": reply
    })

    return "ok"


# ==============================
# SERVER START
# ==============================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
