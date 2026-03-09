import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

user_state = {}

# ---------- SEND MESSAGE ----------

def send_message(chat_id, text, keyboard=None):

    url = f"{TELEGRAM_API}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }

    if keyboard:
        payload["reply_markup"] = {
            "keyboard": keyboard,
            "resize_keyboard": True
        }

    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass


# ---------- MAIN MENU ----------

main_menu = [
["1","2","3"],
["4","5","6"],
["7","8","9"],
["10"]
]

back_button = [["⬅ Back"]]


# ---------- CRYPTO PRICE ----------

def get_crypto_prices():

    try:

        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd"

        data = requests.get(url).json()

        btc = data["bitcoin"]["usd"]
        eth = data["ethereum"]["usd"]
        sol = data["solana"]["usd"]

        return f"""
💰 *Live Crypto Prices*

BTC : ${btc}
ETH : ${eth}
SOL : ${sol}
"""

    except:
        return "Unable to fetch prices."


# ---------- HOME ----------

@app.route("/")
def home():
    return "OpenClaw Bot Running"


# ---------- WEBHOOK ----------

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    if not data:
        return jsonify({"status":"ok"}),200

    message = data.get("message")

    if not message:
        return jsonify({"status":"ok"}),200

    chat_id = message["chat"]["id"]
    text = message.get("text","")

    state = user_state.get(chat_id,"main")


# ---------- START ----------

    if text in ["/start","menu","Menu"]:

        user_state[chat_id] = "main"

        reply = """
🤖 OpenClaw AI Coach

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

        send_message(chat_id, reply, main_menu)


# ---------- LEARN ----------

    elif text == "1":

        reply = """
📚 *Crypto Learning Hub*

Learn the fundamentals of crypto:

• What is blockchain
• Bitcoin basics
• Trading psychology
• Market cycles
"""

        send_message(chat_id, reply, back_button)


# ---------- TRADING ----------

    elif text == "2":

        reply = """
📈 *Trading Strategies*

Popular trading styles:

• Scalping
• Day trading
• Swing trading
• Trend trading
"""

        send_message(chat_id, reply, back_button)


# ---------- RISK ----------

    elif text == "3":

        reply = """
⚠ *Risk Management*

Golden rules:

• Never risk more than 2%
• Always use stop loss
• Protect your capital
"""

        send_message(chat_id, reply, back_button)


# ---------- MARKET ----------

    elif text == "4":

        reply = """
🌍 *Market Analysis*

Understand:

• Bull markets
• Bear markets
• Market sentiment
"""

        send_message(chat_id, reply, back_button)


# ---------- PRICE ----------

    elif text == "5":

        reply = get_crypto_prices()

        send_message(chat_id, reply, back_button)


# ---------- AI ANALYSIS ----------

    elif text == "6":

        reply = """
🤖 *AI Market Insight*

AI analyzes:

• trend strength
• volatility
• market sentiment
"""

        send_message(chat_id, reply, back_button)


# ---------- ALTCOINS ----------

    elif text == "7":

        reply = """
🪙 *Altcoins*

Explore alternative cryptocurrencies beyond Bitcoin.
"""

        send_message(chat_id, reply, back_button)


# ---------- STAKING ----------

    elif text == "8":

        reply = """
🏦 *Staking*

Earn passive income by staking crypto assets.
"""

        send_message(chat_id, reply, back_button)


# ---------- PORTFOLIO ----------

    elif text == "9":

        reply = """
📊 *Portfolio Management*

Build a balanced crypto portfolio.
"""

        send_message(chat_id, reply, back_button)


# ---------- NEWS ----------

    elif text == "10":

        reply = """
📰 *Crypto News*

Stay updated with the latest crypto developments.
"""

        send_message(chat_id, reply, back_button)


# ---------- BACK ----------

    elif text == "⬅ Back":

        user_state[chat_id] = "main"

        reply = """
🤖 OpenClaw AI Coach

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

        send_message(chat_id, reply, main_menu)


    return jsonify({"status":"ok"}),200


# ---------- RUN ----------

if __name__ == "__main__":

    port = int(os.environ.get("PORT",10000))

    app.run(
        host="0.0.0.0",
        port=port
        )
