import os
import requests
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)
@app.route("/", methods=["GET"])
def home():
    return "Bot is running"
ai_mode = {}
memory = {}
# ================= SEND MESSAGE =================

def send(chat, text, keyboard=None):

    data = {
        "chat_id": chat,
        "text": text
    }

    if keyboard:
        data["reply_markup"] = {
            "keyboard": keyboard,
            "resize_keyboard": True
        }

    requests.post(URL + "/sendMessage", json=data)
    # ================= MAIN MENU =================

main_menu = [
["1 Learn","2 Trading"],
["3 Risk","4 Market"],
["5 Price","6 Charts"],
["7 Altcoins","8 Staking"],
["9 Portfolio","10 News"],
["11 AI Assistant"],
["Language"]
]

learn_menu = [
["1.1 What is Blockchain"],
["1.2 What is Bitcoin"],
["1.3 What is Ethereum"],
["⬅ Back"]
]

trading_menu = [
["2.1 Spot Trading"],
["2.2 Futures Trading"],
["2.3 Technical Analysis"],
["⬅ Back"]
]

risk_menu = [
["3.1 Risk Management"],
["3.2 Stop Loss"],
["3.3 Position Size"],
["⬅ Back"]
]

market_menu = [
["4.1 Bull Market"],
["4.2 Bear Market"],
["4.3 Market Cycle"],
["⬅ Back"]
]

price_menu = [
["5.1 BTC Price","5.2 ETH Price"],
["5.3 BNB Price","5.4 SOL Price"],
["⬅ Back"]
]

charts_menu = [
["6.1 BTC Chart"],
["6.2 ETH Chart"],
["6.3 ETH Chart"],
["6.4 SOL Chart"],
["⬅ Back"]
]

altcoins_menu = [
["7.1 What are Altcoins"],
["7.2 Popular Altcoins"],
["7.3 Altcoin Season"],
["⬅ Back"]
]

staking_menu = [
["8.1 What is Staking"],
["8.2 Staking Rewards"],
["8.3 Proof of Stake"],
["⬅ Back"]
]

portfolio_menu = [
["9.1 Diversification"],
["9.2 Long Term Investing"],
["9.3 Portfolio Tracking"],
["9.4 Rebalancing"],
["⬅ Back"]
]

news_menu = [
["10.1 CoinDesk"],
["10.2 CoinTelegraph"],
["10.3 Decrypt"],
["10.4 Binance News"],
["⬅ Back"]
]

language_menu = [
["English","Français","Español"],
["⬅ Back"]
]
# ================= PRICE =================

def get_price(symbol):

    try:
        r = requests.get(
        f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        )

        return r.json()["price"]

    except:
        return "Unavailable"


# ================= LONG EDUCATION TEXT =================

BLOCKCHAIN = """
⛓ WHAT IS BLOCKCHAIN?

Blockchain is a decentralized digital ledger technology used to record transactions across many computers in a secure and transparent way.

Instead of storing information on a central server, blockchain distributes copies of the ledger across many nodes in a network.

Transactions are grouped into blocks. Once verified, the block becomes permanently linked to the previous block using cryptographic hashes.

Because each block references the previous one, altering past information becomes extremely difficult.

This technology provides security, transparency and immutability.

Blockchain is used in cryptocurrencies, finance, supply chain, digital identity systems and decentralized applications.
"""


BITCOIN = """
₿ WHAT IS BITCOIN?

Bitcoin is the first decentralized cryptocurrency created in 2009 by Satoshi Nakamoto.

It allows people to send digital money directly to each other without banks.

Transactions are verified by a distributed network of computers called miners.

Bitcoin operates on a public blockchain where every transaction is permanently recorded.

One of Bitcoin's key features is its limited supply of 21 million coins.

Because of its scarcity and decentralization, Bitcoin is often called digital gold.
"""


ETHEREUM = """
💎 WHAT IS ETHEREUM?

Ethereum is a decentralized blockchain platform launched in 2015 by Vitalik Buterin.

Ethereum allows developers to build decentralized applications called dApps.

It introduced smart contracts which are programs that automatically execute agreements.

These smart contracts power decentralized finance, NFT marketplaces and many Web3 applications.

Today Ethereum is one of the largest blockchain ecosystems in the world.
"""


SPOT = """
📊 SPOT TRADING

Spot trading is the simplest way to trade cryptocurrency.

When you buy a crypto asset on the spot market you immediately receive the asset.

For example if you buy Bitcoin on spot you directly own the Bitcoin.

Spot trading is commonly used for long term investing.

Most crypto exchanges offer hundreds of assets on the spot market.
"""


FUTURES = """
📈 FUTURES TRADING

Futures trading allows traders to speculate on the future price of an asset without owning it.

Traders can open long positions if they expect prices to rise.

They can open short positions if they expect prices to fall.

Futures trading often includes leverage which increases both potential profit and risk.

Because of leverage futures trading is recommended for experienced traders.
"""


TECHNICAL = """
📉 TECHNICAL ANALYSIS

Technical analysis studies charts and historical price data.

Traders analyze indicators such as:

Moving averages
RSI
MACD
Support and resistance

These tools help traders identify trends and possible future price movements.

Technical analysis cannot guarantee results but helps traders make structured decisions.
"""


RISK = """
⚠ RISK MANAGEMENT

Risk management is essential in trading.

It helps protect your capital and reduce losses.

Professional traders usually risk only a small percentage of their capital per trade.

Risk management includes diversification, position sizing and stop losses.
"""


STOP = """
🛑 STOP LOSS

A stop loss automatically closes a trade when price reaches a predefined level.

It protects traders from large unexpected losses.

Using stop loss is one of the most important habits for professional traders.
"""


SIZE = """
📏 POSITION SIZE

Position size refers to the amount of capital allocated to a trade.

Proper position sizing ensures traders do not risk too much money in a single trade.
"""


BULL = """
🐂 BULL MARKET

A bull market is a period where prices are rising and investor confidence is high.

During bull markets investors are optimistic and demand for assets increases.
"""


BEAR = """
🐻 BEAR MARKET

A bear market is a period where prices are falling.

Investor confidence decreases and selling pressure dominates the market.
"""


CYCLE = """
🔄 MARKET CYCLE

Financial markets move in cycles.

Typical cycles include accumulation, uptrend, distribution and downtrend phases.
"""


ALTCOINS = """
🌐 WHAT ARE ALTCOINS?

Altcoins are all cryptocurrencies other than Bitcoin.

Examples include Ethereum, Solana, BNB and many others.

Altcoins often experiment with new blockchain technologies and innovations.
"""


ALTSEASON = """
🚀 ALTCOIN SEASON

Altcoin season happens when many altcoins outperform Bitcoin.

During this phase investors often move capital from Bitcoin into smaller projects.
"""


STAKE = """
💰 STAKING

Staking allows users to earn passive income by locking their crypto to secure a blockchain network.

It is commonly used in Proof of Stake blockchains.
"""


POS = """
🔐 PROOF OF STAKE

Proof of Stake is a consensus mechanism used by many modern blockchains.

Validators lock coins to help validate transactions and secure the network.
"""


PORTFOLIO = """
📊 PORTFOLIO MANAGEMENT

A crypto portfolio is the collection of assets owned by an investor.

Managing a portfolio involves diversification, risk control and long term strategy.
"""
# ================= WEBHOOK =================

@app.route("/", methods=["POST"])
def webhook():

    data = request.get_json()

    if "message" not in data:
        return "ok"

    chat = data["message"]["chat"]["id"]
    text = data["message"].get("text","")

# ================= START =================

    if text == "/start":

        msg = """🚀 Welcome to OpenClaw AI Coach

Your intelligent assistant for learning and exploring cryptocurrency, trading and blockchain technology.

With this bot you can:

📚 Learn crypto fundamentals
📊 Understand trading strategies
📉 Discover risk management techniques
📈 Explore crypto charts
🌐 Learn about altcoins
💰 Understand staking and passive income
📰 Follow crypto news
🤖 Ask the AI Assistant any question

👇 Select a topic from the menu below.
"""

        send(chat, msg, main_menu)
        return "ok"


# ================= BACK =================

    elif text == "⬅ Back":
        send(chat, "Main Menu", main_menu)
        return "ok"


# ================= LEARN =================

    elif text == "1 Learn":
        send(chat, "Choose a topic", learn_menu)
        return "ok"

    elif text == "1.1 What is Blockchain":
        send(chat, BLOCKCHAIN)
        return "ok"

    elif text == "1.2 What is Bitcoin":
        send(chat, BITCOIN)
        return "ok"

    elif text == "1.3 What is Ethereum":
        send(chat, ETHEREUM)
        return "ok"


# ================= TRADING =================

    elif text == "2 Trading":
        send(chat,"Trading Section",trading_menu)
        return "ok"

    elif text == "2.1 Spot Trading":
        send(chat, SPOT)
        return "ok"

    elif text == "2.2 Futures Trading":
        send(chat, FUTURES)
        return "ok"

    elif text == "2.3 Technical Analysis":
        send(chat, TECHNICAL)
        return "ok"


# ================= RISK =================

    elif text == "3 Risk":
        send(chat,"Risk Management Section",risk_menu)
        return "ok"

    elif text == "3.1 Risk Management":
        send(chat, RISK)
        return "ok"

    elif text == "3.2 Stop Loss":
        send(chat, STOP)
        return "ok"

    elif text == "3.3 Position Size":
        send(chat, SIZE)
        return "ok"


# ================= MARKET =================

    elif text == "4 Market":
        send(chat,"Market Education",market_menu)
        return "ok"

    elif text == "4.1 Bull Market":
        send(chat, BULL)
        return "ok"

    elif text == "4.2 Bear Market":
        send(chat, BEAR)
        return "ok"

    elif text == "4.3 Market Cycle":
        send(chat, CYCLE)
        return "ok"
        # ================= PRICE =================

    elif text == "5 Price":
        send(chat,"Crypto Prices",price_menu)
        return "ok"

    elif text == "5.1 BTC Price":
        send(chat, f"BTC Price: ${get_price('BTCUSDT')}")
        return "ok"

    elif text == "5.2 ETH Price":
        send(chat, f"ETH Price: ${get_price('ETHUSDT')}")
        return "ok"

    elif text == "5.3 BNB Price":
        send(chat, f"BNB Price: ${get_price('BNBUSDT')}")
        return "ok"

    elif text == "5.4 SOL Price":
        send(chat, f"SOL Price: ${get_price('SOLUSDT')}")
        return "ok"


# ================= CHARTS =================

    elif text == "6 Charts":
        send(chat,"Crypto Charts",charts_menu)
        return "ok"

    elif text == "6.1 BTC Chart":
        send(chat,"https://www.tradingview.com/symbols/BTCUSDT/")
        return "ok"

    elif text == "6.2 ETH Chart":
        send(chat,"https://www.tradingview.com/symbols/ETHUSDT/")
        return "ok"

    elif text == "6.3 BNB Chart":
        send(chat,"https://www.tradingview.com/symbols/BNBUSDT/")
        return "ok"

    elif text == "6.4 SOL Chart":
        send(chat,"https://www.tradingview.com/symbols/SOLUSDT/")
        return "ok"


# ================= ALTCOINS =================

    elif text == "7 Altcoins":
        send(chat,"Altcoin Education",altcoins_menu)
        return "ok"

    elif text == "7.1 What are Altcoins":
        send(chat, ALTCOINS)
        return "ok"

    elif text == "7.2 Popular Altcoins":
        send(chat, "Popular altcoins include Ethereum, BNB, Solana, XRP and Cardano.")
        return "ok"

    elif text == "7.3 Altcoin Season":
        send(chat, ALTSEASON)
        return "ok"


# ================= STAKING =================

    elif text == "8 Staking":
        send(chat,"Staking Education",staking_menu)
        return "ok"

    elif text == "8.1 What is Staking":
        send(chat, STAKE)
        return "ok"

    elif text == "8.2 Staking Rewards":
        send(chat,"Staking rewards are passive income earned by locking crypto in a network.")
        return "ok"

    elif text == "8.3 Proof of Stake":
        send(chat, POS)
        return "ok"


# ================= PORTFOLIO =================

    elif text == "9 Portfolio":
        send(chat,"Portfolio Management",portfolio_menu)
        return "ok"

    elif text == "9.1 Diversification":
        send(chat,"Diversification spreads investments across different assets to reduce risk.")
        return "ok"

    elif text == "9.2 Long Term Investing":
        send(chat,"Long term investing focuses on holding strong assets for many years.")
        return "ok"

    elif text == "9.3 Portfolio Tracking":
        send(chat,"Portfolio tracking helps investors monitor performance and allocations.")
        return "ok"

    elif text == "9.4 Rebalancing":
        send(chat,"Rebalancing restores your portfolio allocation after market movements.")
        return "ok"
        # ================= NEWS =================

    elif text == "10 News":
        send(chat,"News Sources",news_menu)
        return "ok"

    elif text == "10.1 CoinDesk":
        send(chat,"https://www.coindesk.com")
        return "ok"

    elif text == "10.2 CoinTelegraph":
        send(chat,"https://cointelegraph.com")
        return "ok"

    elif text == "10.3 Decrypt":
        send(chat,"https://decrypt.co")
        return "ok"

    elif text == "10.4 Binance News":
        send(chat,"https://www.binance.com/en/news")
        return "ok"


# ================= LANGUAGE =================

    elif text == "Language":
        send(chat,"Select language",language_menu)
        return "ok"

    elif text == "Français":
        send(chat,"Langue sélectionnée : Français")
        return "ok"

    elif text == "English":
        send(chat,"Language selected: English")
        return "ok"

    elif text == "Español":
        send(chat,"Idioma seleccionado: Español")
        return "ok"


# ================= AI ASSISTANT =================

    elif text == "11 AI Assistant":

        ai_mode[chat] = True
        memory[chat] = []

        send(chat,"🤖 AI Assistant activated. Ask any crypto question.")
        return "ok"


    elif ai_mode.get(chat):

        try:
            send(chat, "🤖 OpenClaw AI is thinking...")

            r = session.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model":"llama3-8b-8192",
                    "messages":[
                        {"role":"system","content":"You are a crypto expert assistant."},
                        {"role":"user","content":text}
                    ]
                },
                timeout=10
            )
            r.raise_for_status()

            reply = r.json()["choices"][0]["message"]["content"]

            send(chat, reply[:4000])

        except:
            send(chat,"⚠ AI unavailable.")

        return "ok"


# ================= END =================

    return "ok"



# ================= SERVER =================

if __name__ == "__main__":

    port = int(os.environ.get("PORT",10000))

    app.run(host="0.0.0.0", port=port)
