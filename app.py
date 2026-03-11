import os
import requests
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

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
# ================= SUB MENUS =================

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
["6.3 BNB Chart"],
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
        r = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
        return r.json()["price"]
    except:
        return "Unavailable"
        # ================= LONG EDUCATION TEXT =================

BLOCKCHAIN = """
⛓ WHAT IS BLOCKCHAIN?

Blockchain is a decentralized digital ledger technology used to record transactions across many computers in a secure and transparent way.

Instead of storing information on a single central server, blockchain distributes copies of the ledger across many nodes in a network. Each node keeps an identical version of the database.

Transactions are grouped into blocks. Once a block is verified, it becomes permanently linked to the previous block using cryptographic hashes. This forms a chain of blocks known as the blockchain.

Because each block references the previous one, altering past information becomes extremely difficult. This provides high security and immutability.

Blockchain technology is now used in many industries including cryptocurrencies, finance, supply chain management, healthcare, digital identity systems and decentralized applications.
"""

BITCOIN = """
₿ WHAT IS BITCOIN?

Bitcoin is the first decentralized cryptocurrency created in 2009 by a mysterious developer known as Satoshi Nakamoto.

It allows users to send digital money directly to each other without relying on banks or financial institutions.

Transactions are verified by a distributed network of computers known as miners. These miners secure the network and confirm transactions by solving complex cryptographic problems.

Bitcoin operates on a public blockchain where every transaction is permanently recorded.

One of Bitcoin's most important features is its limited supply. Only 21 million bitcoins will ever exist, which creates scarcity.

Because of this scarcity and its decentralized nature, Bitcoin is often referred to as "digital gold".
"""

ETHEREUM = """
💎 WHAT IS ETHEREUM?

Ethereum is a decentralized blockchain platform launched in 2015 by Vitalik Buterin and several other developers.

Unlike Bitcoin which mainly focuses on payments, Ethereum allows developers to build decentralized applications known as dApps.

Ethereum introduced the concept of smart contracts. Smart contracts are programs that automatically execute agreements when predefined conditions are met.

This innovation made it possible to build decentralized finance systems, NFT marketplaces, blockchain games and many Web3 applications.

Today Ethereum is one of the largest blockchain ecosystems in the world.
"""
SPOT = """
📊 SPOT TRADING

Spot trading is the simplest way to trade cryptocurrencies.

When you buy a cryptocurrency on the spot market you immediately receive the asset in your wallet or exchange account.

For example if you buy Bitcoin on a spot market you directly own that Bitcoin.

Spot trading is commonly used for long-term investing because traders actually hold the asset.

Most cryptocurrency exchanges offer spot trading for hundreds of digital assets.
"""

FUTURES = """
📈 FUTURES TRADING

Futures trading allows traders to speculate on the future price of a cryptocurrency without owning the actual asset.

Traders can open long positions if they believe the price will rise or short positions if they expect the price to fall.

Futures markets often allow leverage which means traders can control large positions with smaller capital.

While leverage can increase profits it also significantly increases risk.

For this reason futures trading is generally recommended for experienced traders.
"""

TECHNICAL = """
📉 TECHNICAL ANALYSIS

Technical analysis is a method traders use to study financial markets by analyzing price charts and historical data.

Instead of focusing on the fundamental value of an asset, technical analysts study patterns, indicators and price trends.

Common tools include moving averages, RSI indicators, MACD indicators and support and resistance levels.

By analyzing these patterns traders attempt to predict potential future price movements.

Although technical analysis cannot guarantee accuracy, it provides a structured framework for decision making in trading.
"""

RISK = """
⚠ RISK MANAGEMENT

Risk management is one of the most important skills for successful trading.

It involves controlling how much capital you risk on each trade and protecting your portfolio from large losses.

Professional traders often risk only a small percentage of their capital on a single trade.

Risk management techniques include position sizing, diversification and the use of stop losses.

Without proper risk management even skilled traders can lose large amounts of money.
"""
STOP = """
🛑 STOP LOSS

A stop loss is a tool traders use to automatically close a trade when the price reaches a certain level.

Its main purpose is to limit losses and protect trading capital.

For example if you buy Bitcoin at $40,000 you might place a stop loss at $38,000. If the market drops to that level the trade automatically closes.

Using stop losses is one of the most important habits of disciplined traders.
"""

SIZE = """
📏 POSITION SIZE

Position size refers to how much money you allocate to a single trade.

Professional traders calculate position size carefully to control risk.

For example if a trader has $1,000 and only wants to risk 2% per trade, they should not lose more than $20 if the trade fails.

Proper position sizing helps traders survive losing streaks and stay in the market long term.
"""

BULL = """
🐂 BULL MARKET

A bull market describes a period when prices are generally rising and investor confidence is strong.

During a bull market demand for assets increases and prices tend to trend upward over time.

Bull markets often attract new investors because of the positive momentum and media attention.
"""

BEAR = """
🐻 BEAR MARKET

A bear market is the opposite of a bull market.

It occurs when prices decline for an extended period and market sentiment becomes negative.

During bear markets investors may become fearful and many assets lose significant value.

However bear markets can also create opportunities for long-term investors.
"""

CYCLE = """
🔄 MARKET CYCLE

Financial markets often move in cycles.

A typical cycle includes accumulation, uptrend (bull market), distribution and downtrend (bear market).

Understanding market cycles helps investors recognize when markets may be overheated or undervalued.
"""
ALT = """
🪙 ALTCOINS

Altcoins are all cryptocurrencies other than Bitcoin.

The word “altcoin” stands for alternative coin.

Examples include Ethereum, BNB, Solana, XRP and Cardano.

Many altcoins are designed to improve blockchain technology or introduce new features such as smart contracts or faster transactions.
"""

ALT_POP = """
⭐ POPULAR ALTCOINS

Some of the most well-known altcoins include:

Ethereum (ETH) – the largest smart contract platform  
BNB – the native token of the Binance ecosystem  
Solana (SOL) – known for fast transaction speeds  
XRP – focused on cross-border payments  
Cardano (ADA) – a research-driven blockchain platform
"""

ALT_SEASON = """
🚀 ALTCOIN SEASON

Altcoin season occurs when altcoins grow faster than Bitcoin.

During these periods many smaller cryptocurrencies experience large price increases.

Altcoin seasons usually happen after Bitcoin has already made a strong move upward.

Investors then move capital into alternative cryptocurrencies searching for higher returns.
"""

STAKE = """
💰 STAKING

Staking is a process where cryptocurrency holders lock their coins to help secure a blockchain network.

This mechanism is used in Proof-of-Stake blockchains.

Instead of mining, validators confirm transactions and maintain network security.

In return for staking their assets users receive rewards.
"""

STAKE_REWARD = """
🏆 STAKING REWARDS

When users stake their cryptocurrencies they earn rewards from the network.

These rewards are similar to earning interest on savings.

The amount of rewards depends on the blockchain network, the number of coins staked and the duration of staking.
"""

POS = """
⚙ PROOF OF STAKE

Proof of Stake is a blockchain consensus mechanism used to validate transactions.

Instead of miners solving complex puzzles, validators are selected based on the amount of cryptocurrency they stake.

This system reduces energy consumption and improves scalability compared to traditional mining.
"""
DIV = """
📊 DIVERSIFICATION

Diversification is the strategy of spreading investments across different assets.

Instead of putting all capital into a single cryptocurrency, investors distribute funds across multiple assets.

This reduces overall risk because poor performance of one asset may be offset by stronger performance of others.

Diversification is widely used by professional investors to build more stable portfolios.
"""

LONG = """
⏳ LONG TERM INVESTING

Long term investing involves holding assets for extended periods of time.

Instead of trying to predict short-term market movements, investors focus on the long-term growth potential of an asset.

This strategy is common in cryptocurrency where markets can be volatile in the short term but grow significantly over longer periods.
"""

TRACK = """
📈 PORTFOLIO TRACKING

Portfolio tracking involves monitoring the value and performance of your cryptocurrency investments.

Investors track portfolio value, profit and loss, and asset allocation.

Many applications allow users to automatically track their crypto portfolios across multiple exchanges and wallets.
"""

REBAL = """
⚖ PORTFOLIO REBALANCING

Portfolio rebalancing is the process of adjusting the allocation of assets in a portfolio.

Over time some assets grow faster than others which can change the risk level of the portfolio.

Rebalancing restores the desired allocation by selling some assets and buying others.
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
    send(chat, msg, main_menu())
    return "ok"

# ================= LEARN MENU =================

    elif text == "1 Learn":

    keyboard = [
        ["1.1 Blockchain", "1.2 Bitcoin"],
        ["1.3 Ethereum"],
        ["⬅ Back"]
    ]

    send(chat, "Choose a topic", keyboard)
    return "ok"


elif text == "1.1 Blockchain":
    send(chat, BLOCKCHAIN)
    return "ok"


elif text == "1.2 Bitcoin":
    send(chat, BITCOIN)
    return "ok"


elif text == "1.3 Ethereum":
    send(chat, ETHEREUM)
    return "ok"


elif text == "⬅ Back":
    send(chat, "Main Menu", main_menu())
    return "ok"
        # ================= TRADING =================

    elif text == "2 Trading":
        send(chat,"Trading Section",trading_menu)

    elif text == "2.1 Spot Trading":
        send(chat, SPOT)

    elif text == "2.2 Futures Trading":
        send(chat, FUTURES)

    elif text == "2.3 Technical Analysis":
        send(chat, TECHNICAL)


# ================= RISK =================

    elif text == "3 Risk":
        send(chat,"Risk Section",risk_menu)

    elif text == "3.1 Risk Management":
        send(chat, RISK)

    elif text == "3.2 Stop Loss":
        send(chat, STOP)

    elif text == "3.3 Position Size":
        send(chat, SIZE)


# ================= MARKET =================

    elif text == "4 Market":
        send(chat,"Market Section",market_menu)

    elif text == "4.1 Bull Market":
        send(chat, BULL)

    elif text == "4.2 Bear Market":
        send(chat, BEAR)

    elif text == "4.3 Market Cycle":
        send(chat, CYCLE)
        # ================= PRICE =================

    elif text == "5 Price":
        send(chat,"Crypto Prices",price_menu)

    elif text == "5.1 BTC Price":
        send(chat,f"BTC Price: ${get_price('BTCUSDT')}")

    elif text == "5.2 ETH Price":
        send(chat,f"ETH Price: ${get_price('ETHUSDT')}")

    elif text == "5.3 BNB Price":
        send(chat,f"BNB Price: ${get_price('BNBUSDT')}")

    elif text == "5.4 SOL Price":
        send(chat,f"SOL Price: ${get_price('SOLUSDT')}")


# ================= CHARTS =================

    elif text == "6 Charts":
        send(chat,"Charts Section",charts_menu)

    elif text == "6.1 BTC Chart":
        send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT")

    elif text == "6.2 ETH Chart":
        send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:ETHUSDT")

    elif text == "6.3 BNB Chart":
        send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:BNBUSDT")

    elif text == "6.4 SOL Chart":
        send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:SOLUSDT")


# ================= ALTCOINS =================

    elif text == "7 Altcoins":
        send(chat,"Altcoins Section",altcoins_menu)

    elif text == "7.1 What are Altcoins":
        send(chat, ALT)

    elif text == "7.2 Popular Altcoins":
        send(chat, ALT_POP)

    elif text == "7.3 Altcoin Season":
        send(chat, ALT_SEASON)


# ================= STAKING =================

    elif text == "8 Staking":
        send(chat,"Staking Section",staking_menu)

    elif text == "8.1 What is Staking":
        send(chat, STAKE)

    elif text == "8.2 Staking Rewards":
        send(chat, STAKE_REWARD)

    elif text == "8.3 Proof of Stake":
        send(chat, POS)


# ================= PORTFOLIO =================

    elif text == "9 Portfolio":
        send(chat,"Portfolio Section",portfolio_menu)

    elif text == "9.1 Diversification":
        send(chat, DIV)

    elif text == "9.2 Long Term Investing":
        send(chat, LONG)

    elif text == "9.3 Portfolio Tracking":
        send(chat, TRACK)

    elif text == "9.4 Rebalancing":
        send(chat, REBAL)
        # ================= NEWS =================

    elif text == "10 News":
        send(chat,"News Sources",news_menu)
send(chat, DIV)
        return "ok"

    elif text == "9.2 Long Term Investing":
        send(chat, LONG)
        return "ok"

    elif text == "9.3 Portfolio Tracking":
        send(chat, TRACK)
        return "ok"

    elif text == "9.4 Rebalancing":
        send(chat, REBAL)
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

        send(chat,
        "🤖 AI Assistant Activated\n\n"
        "Ask any question about crypto.")

    elif ai_mode.get(chat):

        try:

            history = memory.get(chat, [])

            history.append({"role":"user","content":text})

            messages = [
                {"role":"system",
                 "content":"You are a professional crypto assistant."}
            ] + history[-6:]

            r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
            "Authorization":f"Bearer {GROQ_API_KEY}",
            "Content-Type":"application/json"
            },
            json={
            "model":"llama3-8b-8192",
            "messages":messages
            },
            timeout=20
            )

            data = r.json()

            reply = data["choices"][0]["message"]["content"]

            memory[chat].append({
            "role":"assistant",
            "content":reply
            })

            send(chat,reply[:4000])

        except Exception as e:

            send(chat,"⚠ AI unavailable.")

        return "ok"


    return "ok"


# ================= START SERVER =================

if __name__ == "__main__":

    port = int(os.environ.get("PORT",10000))

    app.run(host="0.0.0.0",port=port)
