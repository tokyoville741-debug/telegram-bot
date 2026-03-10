import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}"

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

user_lang = {}
webhook_set = False
ai_mode = {}

# ===================== MENUS =====================

main_menu = {
"keyboard":[
["1️⃣ Start","2️⃣ Learn"],
["3️⃣ Trading","4️⃣ Risk"],
["5️⃣ Market","6️⃣ Price"],
["7️⃣ Charts","8️⃣ Altcoins"],
["9️⃣ Staking","🔟 Portfolio"],
["1️⃣1️⃣ News","1️⃣2️⃣ AI Assistant"],
["🌐 Language"]
],
"resize_keyboard":True
}

learn_menu = {
"keyboard":[
["2.1 Blockchain","2.2 Bitcoin"],
["2.3 Wallet","2.4 DeFi"],
["⬅ Back"]
],
"resize_keyboard":True
}

trading_menu = {
"keyboard":[
["3.1 Spot Trading","3.2 Futures"],
["3.3 Day Trading","3.4 Swing Trading"],
["⬅ Back"]
],
"resize_keyboard":True
}

risk_menu = {
"keyboard":[
["4.1 Stop Loss","4.2 Position Size"],
["4.3 Risk Reward","4.4 Diversification"],
["⬅ Back"]
],
"resize_keyboard":True
}

market_menu = {
"keyboard":[
["5.1 Bull Market","5.2 Bear Market"],
["5.3 Market Cap","5.4 Liquidity"],
["⬅ Back"]
],
"resize_keyboard":True
}

price_menu = {
"keyboard":[
["6.1 BTC","6.2 ETH"],
["6.3 BNB","6.4 SOL"],
["⬅ Back"]
],
"resize_keyboard":True
}

chart_menu = {
"keyboard":[
["7.1 BTC Chart","7.2 ETH Chart"],
["7.3 BNB Chart","7.4 SOL Chart"],
["⬅ Back"]
],
"resize_keyboard":True
}

alt_menu = {
"keyboard":[
["8.1 Ethereum","8.2 Solana"],
["8.3 Cardano","8.4 Polkadot"],
["⬅ Back"]
],
"resize_keyboard":True
}

staking_menu = {
"keyboard":[
["9.1 What is Staking","9.2 Proof of Stake"],
["9.3 Staking Rewards","9.4 Staking Risks"],
["⬅ Back"]
],
"resize_keyboard":True
}

portfolio_menu = {
"keyboard":[
["10.1 Diversification","10.2 Long Term Investing"],
["10.3 Portfolio Tracking","10.4 Rebalancing"],
["⬅ Back"]
],
"resize_keyboard":True
}

news_menu = {
"keyboard":[
["11.1 CoinDesk","11.2 CoinTelegraph"],
["11.3 Decrypt","11.4 Binance News"],
["⬅ Back"]
],
"resize_keyboard":True
}

language_menu={
"keyboard":[
["English 🇺🇸"],
["Français 🇫🇷"],
["Español 🇪🇸"],
["⬅ Back"]
],
"resize_keyboard":True
}

# ===================== SEND =====================

def send(chat,text,menu=None):

    payload={
    "chat_id":chat,
    "text":text
    }

    if menu:
        payload["reply_markup"]=menu

    requests.post(URL+"/sendMessage",json=payload)

# ===================== PRICE =====================

def price(coin):
    try:

        r = requests.get(
        f"https://api.coinpaprika.com/v1/tickers/{coin}",
        timeout=10
        )

        if r.status_code != 200:
            return "Unavailable"

        data=r.json()
        return round(data["quotes"]["USD"]["price"],2)

    except:
        return "Unavailable"

# ===================== WEB =====================

@app.route("/",methods=["GET"])
def home():
    return "Bot running"

@app.route(f"/{TOKEN}",methods=["POST"])
def bot():

    data=request.json

    if "message" in data:

        chat=data["message"]["chat"]["id"]
        text=data["message"].get("text","")

# ===================== START =====================

        if text=="1️⃣ Start":

            send(chat,
            "Welcome to the Crypto Education Bot.\n\n"
            "This bot teaches cryptocurrency, blockchain, trading strategies, "
            "risk management, market analysis and portfolio management.\n\n"
            "Select a topic from the menu below to start learning.",
            main_menu)

# ===================== LEARN =====================

        elif text=="2️⃣ Learn":

            send(chat,
            "2️⃣ Crypto Learning\n\n"
            "Select a lesson to begin learning about blockchain and crypto.",
            learn_menu)

# ===================== TRADING =====================

        elif text=="3️⃣ Trading":

            send(chat,
            "3️⃣ Trading Strategies\n\n"
            "Learn how traders buy and sell crypto assets.",
            trading_menu)

# ===================== RISK =====================

        elif text=="4️⃣ Risk":

            send(chat,
            "4️⃣ Risk Management\n\n"
            "Risk management protects traders from large losses.",
            risk_menu)

# ===================== MARKET =====================

        elif text=="5️⃣ Market":

            send(chat,
            "5️⃣ Market Analysis\n\n"
            "Understanding the crypto market helps investors make better decisions.",
            market_menu)

# ===================== PRICE =====================

        elif text=="6️⃣ Price":

            send(chat,
            "6️⃣ Cryptocurrency Prices\n\nSelect a cryptocurrency.",
            price_menu)

        elif text=="6.1 BTC":
            send(chat,f"Bitcoin Price: ${price('btc-bitcoin')}")

        elif text=="6.2 ETH":
            send(chat,f"Ethereum Price: ${price('eth-ethereum')}")

        elif text=="6.3 BNB":
            send(chat,f"BNB Price: ${price('bnb-binance-coin')}")

        elif text=="6.4 SOL":
            send(chat,f"Solana Price: ${price('sol-solana')}")

# ===================== CHARTS =====================

        elif text=="7️⃣ Charts":

            send(chat,
            "7️⃣ Crypto Charts\n\n"
            "Charts help traders analyze price movements "
            "and identify trends in the market.\n\n"
            "Select a chart to open it on TradingView.",
            chart_menu)

        elif text=="7.1 BTC Chart":
            send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT")

        elif text=="7.2 ETH Chart":
            send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:ETHUSDT")

        elif text=="7.3 BNB Chart":
            send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:BNBUSDT")

        elif text=="7.4 SOL Chart":
            send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:SOLUSDT")

# ===================== NEWS =====================

        elif text=="1️⃣1️⃣ News":

            send(chat,
            "1️⃣1️⃣ Crypto News Sources\n\nSelect a news source.",
            news_menu)

        elif text=="11.1 CoinDesk":
            send(chat,"https://www.coindesk.com")

        elif text=="11.2 CoinTelegraph":
            send(chat,"https://cointelegraph.com")

        elif text=="11.3 Decrypt":
            send(chat,"https://decrypt.co")

        elif text=="11.4 Binance News":
            send(chat,"https://www.binance.com/en/news")

# ===================== AI =====================

        elif text=="1️⃣2️⃣ AI Assistant":

            send(chat,
            "1️⃣2️⃣ AI Assistant\n\nAsk any cryptocurrency question.")

# ===================== BACK =====================

        elif text=="⬅ Back":

            send(chat,"Main Menu",main_menu)

    return "ok"

# ===================== WEBHOOK =====================

@app.before_request
def setup_webhook():

    global webhook_set

    if not webhook_set:

        url=os.environ.get("RENDER_EXTERNAL_URL")+f"/{TOKEN}"

        requests.get(URL+"/setWebhook",params={"url":url})

        webhook_set=True

# ===================== RUN =====================

if __name__=="__main__":

    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
