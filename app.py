import os
import requests
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

ai_mode = {}

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

A stop loss is an automatic order that closes a trade when the price reaches a specific level.

It is designed to limit potential losses.

For example if you buy Bitcoin at $60,000 you may place a stop loss at $58,000.

If the market drops to that level your position automatically closes.

Stop losses help remove emotions from trading decisions and protect your capital.
"""

SIZE = """
📏 POSITION SIZE

Position sizing determines how much capital you allocate to each trade.

Instead of risking your entire portfolio on one trade, experienced traders divide their capital across multiple trades.

Many traders follow the 1% or 2% rule meaning they risk only 1–2% of their total capital per trade.

Proper position sizing prevents a single losing trade from destroying your portfolio.
"""

BULL = """
📈 BULL MARKET

A bull market is a period where asset prices rise consistently over time.

During bull markets investor confidence is high and demand for assets increases.

Bull markets are often driven by strong economic conditions, technological innovation and positive investor sentiment.

Cryptocurrency bull markets have historically produced large price increases across many digital assets.
"""

BEAR = """
📉 BEAR MARKET

A bear market is a prolonged period where asset prices decline and investor sentiment becomes pessimistic.

During bear markets traders often experience fear and uncertainty.

Prices may fall significantly before the market eventually stabilizes and begins a new cycle.

Bear markets are a natural part of financial markets and often follow major bull runs.
"""

CYCLE = """
🔄 MARKET CYCLE

Financial markets move in cycles rather than straight lines.

A typical market cycle has four phases:

1. Accumulation – smart investors slowly buy assets
2. Uptrend (Markup) – prices rise rapidly
3. Distribution – early investors begin selling
4. Downtrend (Markdown) – prices decline

Understanding market cycles helps traders identify opportunities and manage risk.
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

Diversification is the practice of spreading investments across multiple assets.

Instead of putting all capital into a single cryptocurrency, investors distribute funds across several assets.

This strategy reduces risk because poor performance from one asset can be balanced by gains in another.
"""

LONG = """
📈 LONG TERM INVESTING

Long term investing focuses on holding assets for years rather than trading frequently.

Investors believe the value of strong projects will increase over time.

This strategy avoids emotional trading and reduces transaction costs.
"""

TRACK = """
📊 PORTFOLIO TRACKING

Portfolio tracking helps investors monitor the performance of their investments.

By tracking asset values, profits and losses investors can better understand how their portfolio evolves over time.

Many investors use tracking tools to manage risk and evaluate investment strategies.
"""

REBAL = """
⚖ REBALANCING

Rebalancing means adjusting the proportions of assets in your portfolio.

If one asset grows significantly it may represent too large a percentage of your portfolio.

Rebalancing involves selling part of the outperforming asset and buying others to maintain a balanced allocation.

This strategy helps control risk and maintain a consistent investment strategy.
"""
# ================= BOT =================

@app.route(f"/{TOKEN}", methods=["POST"])
def bot():

    data = request.get_json()

    if not data or "message" not in data:
        return "ok"

    chat = data["message"]["chat"]["id"]
    text = data["message"].get("text","")

# START

    if text == "/start":

        ai_mode[chat] = False

        send(chat,

"🚀 Welcome to OpenClaw AI Coach\n\n"
"Your intelligent assistant for learning and exploring cryptocurrency, trading and blockchain technology.\n\n"
"With this bot you can:\n"
"📚 Learn crypto fundamentals\n"
"📊 Understand trading strategies\n"
"📉 Discover risk management techniques\n"
"📈 Explore crypto charts\n"
"🪙 Learn about altcoins\n"
"💰 Understand staking and passive income\n"
"📰 Follow crypto news\n"
"🤖 Ask the AI Assistant any question\n\n"
"👇 Select a topic from the menu below.",
main_menu)

# BACK

    elif text == "⬅ Back":

        ai_mode[chat] = False
        send(chat,"Main Menu",main_menu)

# MENUS

    elif text == "1 Learn":
        send(chat,"Learning Section",learn_menu)

    elif text == "2 Trading":
        send(chat,"Trading Section",trading_menu)

    elif text == "3 Risk":
        send(chat,"Risk Section",risk_menu)

    elif text == "4 Market":
        send(chat,"Market Section",market_menu)

    elif text == "5 Price":
        send(chat,"Crypto Prices",price_menu)

    elif text == "6 Charts":
        send(chat,"Charts Section",charts_menu)

    elif text == "7 Altcoins":
        send(chat,"Altcoins Section",altcoins_menu)

    elif text == "8 Staking":
        send(chat,"Staking Section",staking_menu)

    elif text == "9 Portfolio":
        send(chat,"Portfolio Section",portfolio_menu)

    elif text == "10 News":
        send(chat,"News Sources",news_menu)

    elif text == "Language":
        send(chat,"Select language",language_menu)

# EDUCATION

    elif text == "1.1 What is Blockchain":
        send(chat,BLOCKCHAIN)

    elif text == "1.2 What is Bitcoin":
        send(chat,BITCOIN)

    elif text == "1.3 What is Ethereum":
        send(chat,ETHEREUM)

# PRICES

    elif text == "5.1 BTC Price":
        send(chat,f"BTC Price: ${get_price('BTCUSDT')}")

    elif text == "5.2 ETH Price":
        send(chat,f"ETH Price: ${get_price('ETHUSDT')}")

    elif text == "5.3 BNB Price":
        send(chat,f"BNB Price: ${get_price('BNBUSDT')}")

    elif text == "5.4 SOL Price":
        send(chat,f"SOL Price: ${get_price('SOLUSDT')}")

# CHARTS

    elif text == "6.1 BTC Chart":
        send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT")

    elif text == "6.2 ETH Chart":
        send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:ETHUSDT")

    elif text == "6.3 BNB Chart":
        send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:BNBUSDT")

    elif text == "6.4 SOL Chart":
        send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:SOLUSDT")

# NEWS (CORRIGÉ)

    elif text == "10.1 CoinDesk":
        send(chat,"https://www.coindesk.com")

    elif text == "10.2 CoinTelegraph":
        send(chat,"https://cointelegraph.com")

    elif text == "10.3 Decrypt":
        send(chat,"https://decrypt.co")

    elif text == "10.4 Binance News":
        send(chat,"https://www.binance.com/en/news")

# AI

    elif text == "11 AI Assistant":

        ai_mode[chat] = True
        send(chat,"🤖 AI Assistant Activated\nAsk any question about crypto.")

    elif ai_mode.get(chat):

        try:

            r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
            "Authorization":f"Bearer {GROQ_API_KEY}",
            "Content-Type":"application/json"
            },
            json={
            "model":"llama3-8b-8192",
            "messages":[{"role":"user","content":text}]
            })

            reply = r.json()["choices"][0]["message"]["content"]

            send(chat,reply[:4000])

        except:

            send(chat,"⚠ AI unavailable.")

    return "ok"

if __name__ == "__main__":

    port = int(os.environ.get("PORT",10000))

    app.run(host="0.0.0.0",port=port)
