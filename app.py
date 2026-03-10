import os
import requests
import threading
import time
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

ai_mode={}
webhook_set=False


# ================= SEND MESSAGE =================

def send(chat,text,keyboard=None):

    data={
        "chat_id":chat,
        "text":text
    }

    if keyboard:
        data["reply_markup"]={
            "keyboard":keyboard,
            "resize_keyboard":True
        }

    requests.post(URL+"/sendMessage",json=data)



# ================= MAIN MENU =================

main_menu=[
["1 Learn","2 Trading"],
["3 Risk","4 Market"],
["5 Price","6 Charts"],
["7 Altcoins","8 Staking"],
["9 Portfolio","10 News"],
["11 AI Assistant"],
["Language"]
]


# ================= SUB MENUS =================

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


price_menu=[
["5.1 BTC Price","5.2 ETH Price"],
["5.3 BNB Price","5.4 SOL Price"],
["⬅ Back"]
]


charts_menu=[
["6.1 BTC Chart","6.2 ETH Chart"],
["6.3 BNB Chart","6.4 SOL Chart"],
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


portfolio_menu=[
["9.1 Diversification"],
["9.2 Long Term Investing"],
["9.3 Portfolio Tracking"],
["9.4 Rebalancing"],
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
["English","Français"],
["Español"],
["⬅ Back"]
]



# ================= PRICE FUNCTION =================

def get_price(symbol):

    try:

        r=requests.get(
        f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        )

        return r.json()["price"]

    except:

        return "Unavailable"
        # ================= EDUCATIONAL TEXTS =================  


BLOCKCHAIN_TEXT = """
⛓ WHAT IS BLOCKCHAIN?

Blockchain is a decentralized digital ledger technology that records transactions across many computers in a secure and transparent way. Instead of storing information in a single central server, blockchain distributes the data across a network of computers called nodes.

Each transaction is grouped together into a block. Once a block is verified, it is linked to the previous block, forming a continuous chain of records known as the blockchain. This structure makes it extremely difficult to alter or delete past transactions.

One of the most important characteristics of blockchain technology is decentralization. No single authority controls the entire system. This reduces the risk of corruption, manipulation, or single points of failure.

Blockchain also provides transparency. Most public blockchains allow anyone to verify transactions, which increases trust between users who do not know each other.

Security is achieved through cryptography. Every transaction is protected by advanced mathematical algorithms that ensure only valid transactions are recorded.

Because of these properties, blockchain technology is used not only for cryptocurrencies but also in industries such as finance, healthcare, logistics, gaming, and digital identity systems.
"""


BITCOIN_TEXT = """
₿ WHAT IS BITCOIN?

Bitcoin is the first cryptocurrency ever created and remains the most widely recognized digital asset in the world. It was introduced in 2009 by an anonymous person or group using the name Satoshi Nakamoto.

The main goal of Bitcoin was to create a decentralized digital currency that allows people to send money directly to each other without needing banks or financial intermediaries.

Bitcoin operates on a blockchain network where transactions are verified by participants known as miners. These miners use computing power to validate transactions and secure the network.

One of the most important features of Bitcoin is its limited supply. Only 21 million bitcoins will ever exist. This scarcity is one reason why many investors compare Bitcoin to digital gold.

Bitcoin is commonly used as a store of value, a payment method, and a long-term investment asset in the cryptocurrency ecosystem.
"""


ETHEREUM_TEXT = """
💎 WHAT IS ETHEREUM?

Ethereum is a blockchain platform that allows developers to build decentralized applications, also known as dApps. It was created in 2015 by Vitalik Buterin and several other developers.

While Bitcoin focuses mainly on digital payments, Ethereum was designed to be a programmable blockchain. This means developers can create applications that run directly on the blockchain without relying on centralized servers.

One of Ethereum's most important innovations is the concept of smart contracts. Smart contracts are self-executing programs that automatically carry out agreements when certain conditions are met.

These smart contracts power many areas of the crypto ecosystem including decentralized finance (DeFi), NFT marketplaces, blockchain games, and decentralized autonomous organizations (DAOs).

Ethereum has become the foundation for thousands of crypto projects and remains one of the most influential platforms in the blockchain industry.
"""


SPOT_TRADING_TEXT = """
📊 SPOT TRADING

Spot trading is the most basic and common form of cryptocurrency trading. In spot trading, traders buy or sell cryptocurrencies at the current market price, and the transaction is settled immediately.

When you purchase a cryptocurrency through spot trading, the asset is transferred directly to your account. This means you fully own the asset and can hold it, sell it, or transfer it to another wallet.

Spot trading is considered beginner-friendly because it does not involve complex financial instruments like leverage or derivatives.

Most major cryptocurrency exchanges such as Binance, Coinbase, and Kraken offer spot markets for hundreds of different cryptocurrencies.

Traders often use spot trading to accumulate assets for long-term investment or to take advantage of short-term price movements.
"""


FUTURES_TRADING_TEXT = """
📈 FUTURES TRADING

Futures trading is a more advanced type of trading that allows traders to speculate on the future price of a cryptocurrency without actually owning the asset.

In futures trading, traders enter contracts that bet on whether the price of a cryptocurrency will go up or down. These contracts can use leverage, which means traders can control a larger position with a smaller amount of capital.

While leverage can increase potential profits, it also significantly increases risk. If the market moves against a trader's position, losses can occur very quickly.

Because of these risks, futures trading is usually recommended only for experienced traders who fully understand market volatility and risk management strategies.

Many professional traders use futures trading to hedge positions or profit from both rising and falling markets.
"""


TECHNICAL_ANALYSIS_TEXT = """
📉 TECHNICAL ANALYSIS

Technical analysis is a method used by traders to evaluate financial markets by studying historical price movements and trading volume.

Instead of focusing on news or fundamental value, technical analysis focuses on chart patterns, trends, and technical indicators.

Common tools used in technical analysis include moving averages, RSI (Relative Strength Index), MACD indicators, and support and resistance levels.

By analyzing these patterns, traders attempt to predict potential future price movements and identify trading opportunities.

Although technical analysis does not guarantee accurate predictions, it provides traders with structured tools for making more informed trading decisions.
"""


RISK_MANAGEMENT_TEXT = """
⚠ RISK MANAGEMENT

Risk management is one of the most important aspects of successful trading and investing. It involves strategies that help traders protect their capital and minimize potential losses.

One key principle of risk management is never risking more money than you can afford to lose. Markets can be highly volatile, and unexpected events can cause sudden price movements.

Traders often use techniques such as stop-loss orders, proper position sizing, and diversification to reduce risk exposure.

Good risk management allows traders to survive losing trades and remain active in the market over the long term.

Without proper risk management, even a skilled trader can lose their entire capital due to a few bad trades.
"""


STOP_LOSS_TEXT = """
🛑 STOP LOSS

A stop loss is a predefined price level at which a trade is automatically closed to prevent further losses.

For example, if a trader buys Bitcoin at $60,000, they might set a stop loss at $58,000. If the market drops to that level, the position is automatically sold.

Stop losses help traders remove emotions from trading decisions and enforce discipline.

Professional traders almost always set stop-loss levels before entering a trade to ensure they control the amount of risk they take.
"""


POSITION_SIZE_TEXT = """
📏 POSITION SIZE

Position sizing refers to the amount of capital allocated to a single trade. Proper position sizing helps traders manage risk and avoid large losses.

Instead of investing all available funds into one trade, experienced traders divide their capital across multiple trades.

A common rule among professional traders is the 1–2% rule, which means risking only 1% or 2% of total capital on a single trade.

By controlling position size, traders ensure that a single losing trade does not significantly damage their overall portfolio.
"""
# ================= BOT =================

@app.route(f"/{TOKEN}", methods=["POST"])
def bot():

    data = request.get_json()

    if not data or "message" not in data:
        return "ok"

    chat = data["message"]["chat"]["id"]
    text = data["message"].get("text","")


# ================= START =================

    if text=="/start":

        ai_mode[chat]=False

        send(chat,
        "🚀 Welcome to OpenClaw AI Coach\n\n"
        "Your intelligent assistant for learning and exploring the world of cryptocurrency, trading, and blockchain technology.\n\n"
        "With OpenClaw AI Coach you can:\n"
        "📚 Learn crypto fundamentals\n"
        "📊 Understand trading strategies\n"
        "📉 Discover risk management techniques\n"
        "📈 Explore crypto charts\n"
        "🪙 Learn about altcoins\n"
        "💰 Understand staking and passive income\n"
        "📰 Stay updated with crypto news\n"
        "🤖 Ask the AI Assistant any question\n\n"
        "Whether you are a beginner or an experienced trader, this bot will help you understand the crypto ecosystem step by step.\n\n"
        "👇 Select a topic from the menu below.",
        main_menu)


# ================= BACK =================

    elif text=="⬅ Back":

        ai_mode[chat]=False
        send(chat,"Main Menu",main_menu)


# ================= LANGUAGE =================

    elif text=="Language":

        send(chat,
        "🌍 Select your language / Choisissez votre langue / Seleccione su idioma",
        language_menu)

    elif text=="English":
        send(chat,"Language set to English.")

    elif text=="Français":
        send(chat,"Langue définie sur Français.")

    elif text=="Español":
        send(chat,"Idioma configurado en Español.")


# ================= AI ASSISTANT =================

    elif text=="11 AI Assistant":

        ai_mode[chat]=True

        send(chat,
        "🤖 AI Assistant Activated\n\n"
        "Ask any question about cryptocurrency, trading or blockchain.")


# ================= AI RESPONSE =================

    elif ai_mode.get(chat):

        try:

            r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
            "Authorization":f"Bearer {GROQ_API_KEY}",
            "Content-Type":"application/json"
            },
            json={
            "model":"llama3-70b-8192",
            "messages":[
            {"role":"user","content":text}
            ]
            })

            reply = r.json()["choices"][0]["message"]["content"]

            send(chat,reply[:4000])

        except:

            send(chat,"⚠ AI unavailable.")


    return "ok"
