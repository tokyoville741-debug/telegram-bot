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

price_menu=[
["5.1 BTC Price","5.2 ETH Price"],
["5.3 BNB Price","5.4 SOL Price"],
["⬅ Back"]
]

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
        "This bot helps you learn cryptocurrency, understand trading, "
        "manage risk, explore altcoins, track prices and read crypto news.\n\n"
        "Use the menu below to navigate through the different crypto topics.",
        main_menu)


# ================= BACK =================

    elif text=="⬅ Back":

        ai_mode[chat]=False

        send(chat,"Main Menu",main_menu)


# ================= LEARN =================

    elif text=="1 Learn":

        send(chat,"Crypto Learning Section",learn_menu)

    elif text=="1.1 What is Blockchain":

        send(chat,"Blockchain is a decentralized ledger that records transactions securely.")

    elif text=="1.2 What is Bitcoin":

        send(chat,"Bitcoin is the first cryptocurrency created in 2009.")

    elif text=="1.3 What is Ethereum":

        send(chat,"Ethereum allows smart contracts and decentralized applications.")


# ================= TRADING =================

    elif text=="2 Trading":

        send(chat,"Trading topics.",trading_menu)

    elif text=="2.1 Spot Trading":

        send(chat,"Spot trading is buying and selling crypto at market price.")

    elif text=="2.2 Futures Trading":

        send(chat,"Futures trading allows leverage and speculation.")

    elif text=="2.3 Technical Analysis":

        send(chat,"Technical analysis studies charts and indicators.")


# ================= RISK =================

    elif text=="3 Risk":

        send(chat,"Risk management topics.",risk_menu)

    elif text=="3.1 Risk Management":

        send(chat,"Risk management protects capital.")

    elif text=="3.2 Stop Loss":

        send(chat,"Stop loss closes a trade automatically.")

    elif text=="3.3 Position Size":

        send(chat,"Position sizing controls risk per trade.")


# ================= MARKET =================

    elif text=="4 Market":

        send(chat,"Market concepts.",market_menu)

    elif text=="4.1 Bull Market":

        send(chat,"Bull market means rising prices.")

    elif text=="4.2 Bear Market":

        send(chat,"Bear market means falling prices.")

    elif text=="4.3 Market Cycle":

        send(chat,"Markets move in cycles.")


# ================= PRICE =================

    elif text=="5 Price":

        send(chat,"Crypto Prices",price_menu)

    elif text=="5.1 BTC Price":

        price=get_price("BTCUSDT")
        send(chat,f"BTC Price: ${price}")

    elif text=="5.2 ETH Price":

        price=get_price("ETHUSDT")
        send(chat,f"ETH Price: ${price}")

    elif text=="5.3 BNB Price":

        price=get_price("BNBUSDT")
        send(chat,f"BNB Price: ${price}")

    elif text=="5.4 SOL Price":

        price=get_price("SOLUSDT")
        send(chat,f"SOL Price: ${price}")


# ================= CHARTS =================

    elif text=="6 Charts":

        send(chat,"Trading charts.",charts_menu)

    elif text=="6.1 BTC Chart":

        send(chat,"https://www.tradingview.com/symbols/BTCUSDT/")

    elif text=="6.2 ETH Chart":

        send(chat,"https://www.tradingview.com/symbols/ETHUSDT/")

    elif text=="6.3 BNB Chart":

        send(chat,"https://www.tradingview.com/symbols/BNBUSDT/")

    elif text=="6.4 SOL Chart":

        send(chat,"https://www.tradingview.com/symbols/SOLUSDT/")


# ================= ALTCOINS =================

    elif text=="7 Altcoins":

        send(chat,"Altcoins topics.",altcoins_menu)

    elif text=="7.1 What are Altcoins":

        send(chat,"Altcoins are cryptocurrencies other than Bitcoin.")

    elif text=="7.2 Popular Altcoins":

        send(chat,"Examples include Ethereum, BNB, Solana.")

    elif text=="7.3 Altcoin Season":

        send(chat,"Altcoin season is when altcoins outperform BTC.")


# ================= STAKING =================

    elif text=="8 Staking":

        send(chat,"Staking topics.",staking_menu)

    elif text=="8.1 What is Staking":

        send(chat,"Staking locks crypto to support blockchain security.")

    elif text=="8.2 Staking Rewards":

        send(chat,"Users earn rewards by staking.")

    elif text=="8.3 Proof of Stake":

        send(chat,"PoS is a blockchain consensus mechanism.")


# ================= PORTFOLIO =================

    elif text=="9 Portfolio":

        send(chat,"Portfolio management.",portfolio_menu)

    elif text=="9.1 Diversification":

        send(chat,"Diversification spreads risk across assets.")

    elif text=="9.2 Long Term Investing":

        send(chat,"Long term investors hold assets for years.")

    elif text=="9.3 Portfolio Tracking":

        send(chat,"Tracking monitors performance.")

    elif text=="9.4 Rebalancing":

        send(chat,"Rebalancing maintains asset allocation.")


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


# ================= LANGUAGE =================

    elif text=="Language":

        send(chat,"Choose language.",language_menu)


    return "ok"


# ================= WEBHOOK =================

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
