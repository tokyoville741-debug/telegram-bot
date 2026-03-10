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


# ================= SEND =================

def send(chat,text,keyboard=None):

    data={"chat_id":chat,"text":text}

    if keyboard:
        data["reply_markup"]={
            "keyboard":keyboard,
            "resize_keyboard":True
        }

    requests.post(URL+"/sendMessage",json=data)


# ================= MENUS =================

main_menu=[
["1 Learn","2 Trading"],
["3 Risk","4 Market"],
["5 Price","6 Charts"],
["7 Altcoins","8 Staking"],
["9 Portfolio","10 News"],
["11 AI Assistant"],
["Language"]
]

learn_menu=[
["1.1 What is Blockchain"],
["1.2 What is Bitcoin"],
["1.3 What is Ethereum"],
["⬅ Back"]
]

trading_menu=[
["2.1 Spot Trading"],
["2.2 Futures Trading"],
["2.3 Technical Analysis"],
["⬅ Back"]
]

risk_menu=[
["3.1 Risk Management"],
["3.2 Stop Loss"],
["3.3 Position Size"],
["⬅ Back"]
]

market_menu=[
["4.1 Bull Market"],
["4.2 Bear Market"],
["4.3 Market Cycle"],
["⬅ Back"]
]

altcoins_menu=[
["7.1 What are Altcoins"],
["7.2 Popular Altcoins"],
["7.3 Altcoin Season"],
["⬅ Back"]
]

staking_menu=[
["8.1 What is Staking"],
["8.2 Staking Rewards"],
["8.3 Proof of Stake"],
["⬅ Back"]
]

# PRICE MENU (corrigé)

price_menu=[
["5.1 BTC Price","5.2 ETH Price"],
["5.3 BNB Price","5.4 SOL Price"],
["⬅ Back"]
]

# PORTFOLIO MENU (corrigé)

portfolio_menu=[
["9.1 Diversification"],
["9.2 Long Term Investing"],
["9.3 Portfolio Tracking"],
["9.4 Rebalancing"],
["⬅ Back"]
]

charts_menu=[
["6.1 BTC Chart","6.2 ETH Chart"],
["6.3 BNB Chart","6.4 SOL Chart"],
["⬅ Back"]
]

news_menu=[
["10.1 CoinDesk"],
["10.2 CoinTelegraph"],
["10.3 Decrypt"],
["10.4 Binance News"],
["⬅ Back"]
]

language_menu=[
["English"],
["Français"],
["Español"],
["⬅ Back"]
]


# ================= PRICE FUNCTION =================

def get_price(symbol):

    try:

        r=requests.get(
        f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        )

        price=r.json()["price"]

        return price

    except:

        return "Unavailable"


# ================= WEBHOOK =================

@app.route(f"/{TOKEN}",methods=["POST"])
def bot():

    data=request.get_json()

    if "message" not in data:
        return "ok"

    chat=data["message"]["chat"]["id"]
    text=data["message"].get("text","")


# ================= START =================

    if text=="/start":

        ai_mode[chat]=False

        send(chat,
        "🚀 Welcome to OpenClaw AI Coach\n\n"
        "Your intelligent assistant for learning cryptocurrency, "
        "trading strategies, and blockchain technology.\n\n"
        "Use the menu below to explore different crypto topics "
        "including trading, risk management, charts, staking, "
        "altcoins and more.",
        main_menu)


# ================= BACK =================

    elif text=="⬅ Back":

        ai_mode[chat]=False

        send(chat,"Main Menu",main_menu)


# ================= PRICE =================

    elif text=="5 Price":

        send(chat,
        "💰 Crypto Prices\n\n"
        "Select a cryptocurrency to view its current market price.",
        price_menu)

    elif text=="5.1 BTC Price":

        price=get_price("BTCUSDT")

        send(chat,f"₿ Bitcoin Price\n\nCurrent BTC price:\n${price}")

    elif text=="5.2 ETH Price":

        price=get_price("ETHUSDT")

        send(chat,f"💎 Ethereum Price\n\nCurrent ETH price:\n${price}")

    elif text=="5.3 BNB Price":

        price=get_price("BNBUSDT")

        send(chat,f"🟡 BNB Price\n\nCurrent BNB price:\n${price}")

    elif text=="5.4 SOL Price":

        price=get_price("SOLUSDT")

        send(chat,f"🟣 Solana Price\n\nCurrent SOL price:\n${price}")


# ================= PORTFOLIO =================

    elif text=="9 Portfolio":

        send(chat,
        "📊 Crypto Portfolio Management\n\n"
        "A crypto portfolio is the collection of digital assets "
        "that an investor holds. Managing a portfolio correctly "
        "is important to reduce risk and maximize long-term returns.\n\n"
        "Good portfolio management includes diversification, "
        "long-term strategy, tracking investments and regular "
        "rebalancing.",
        portfolio_menu)

    elif text=="9.1 Diversification":

        send(chat,
        "📊 Diversification\n\n"
        "Diversification means spreading your investment across "
        "different cryptocurrencies instead of putting all your "
        "money into a single asset.\n\n"
        "This strategy reduces risk because if one asset performs "
        "poorly, others may still perform well.\n\n"
        "A diversified portfolio often includes:\n"
        "• Bitcoin\n"
        "• Ethereum\n"
        "• Large-cap altcoins\n"
        "• Emerging projects.")

    elif text=="9.2 Long Term Investing":

        send(chat,
        "⏳ Long-Term Investing\n\n"
        "Long-term investing focuses on holding cryptocurrencies "
        "for months or years instead of trading frequently.\n\n"
        "This strategy allows investors to benefit from long-term "
        "growth of the crypto market and avoid emotional trading.")

    elif text=="9.3 Portfolio Tracking":

        send(chat,
        "📈 Portfolio Tracking\n\n"
        "Tracking your portfolio helps you monitor how your "
        "investments perform over time.\n\n"
        "Investors usually track:\n"
        "• Asset allocation\n"
        "• Profit and loss\n"
        "• Market value\n"
        "• Performance trends.")

    elif text=="9.4 Rebalancing":

        send(chat,
        "⚖️ Portfolio Rebalancing\n\n"
        "Rebalancing means adjusting your portfolio periodically "
        "to maintain the desired asset allocation.\n\n"
        "For example, if Bitcoin grows too large in your portfolio, "
        "you may sell a small portion and redistribute the funds "
        "into other assets.")


# ================= OTHER PARTS (INCHANGED) =================

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


    return "ok"


# ================= WEBHOOK SETUP =================

@app.before_request
def setup_webhook():

    global webhook_set

    if not webhook_set:

        url=os.environ.get("RENDER_EXTERNAL_URL")+f"/{TOKEN}"

        requests.get(URL+"/setWebhook",params={"url":url})

        webhook_set=True


# ================= KEEP ALIVE =================

def keep_alive():

    while True:

        try:
            requests.get(os.environ.get("RENDER_EXTERNAL_URL"))
        except:
            pass

        time.sleep(300)

threading.Thread(target=keep_alive).start()


# ================= RUN =================

if __name__=="__main__":

    port=int(os.environ.get("PORT",10000))

    app.run(host="0.0.0.0",port=port)
