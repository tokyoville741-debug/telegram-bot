import requests
import time

TOKEN = "TON_TOKEN_ICI"
URL = f"https://api.telegram.org/bot{TOKEN}/"

# MENUS
main_menu = {
    "keyboard":[
        ["📚 Learn","📈 Trading"],
        ["⚠ Risk","📊 Market"],
        ["💰 Price","📊 Charts"],
        ["🌕 Altcoins","🔒 Staking"],
        ["💼 Portfolio","📰 News"],
        ["🧠 AI Assistant"]
    ],
    "resize_keyboard":True
}

price_menu = {
    "keyboard":[
        ["BTC","ETH"],
        ["SOL","BNB"],
        ["⬅ Back"]
    ],
    "resize_keyboard":True
}

chart_menu = {
    "keyboard":[
        ["BTC Chart","ETH Chart"],
        ["SOL Chart","BNB Chart"],
        ["⬅ Back"]
    ],
    "resize_keyboard":True
}

back_menu = {
    "keyboard":[["⬅ Back"]],
    "resize_keyboard":True
}


def send(chat_id,text,keyboard=None):

    data = {
        "chat_id":chat_id,
        "text":text
    }

    if keyboard:
        data["reply_markup"]=keyboard

    try:
        requests.post(URL+"sendMessage",json=data)
    except:
        pass


def price(coin):

    try:
        r = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        )

        data = r.json()

        return data.get(coin,{}).get("usd","Unavailable")

    except:
        return "Unavailable"


def crypto_news():

    try:

        r = requests.get(
            "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
        )

        news = r.json().get("Data",[])[:5]

        text = "📰 Latest Crypto News\n\n"

        for n in news:

            title = n.get("title","")
            url = n.get("url","")

            text += f"{title}\n{url}\n\n"

        return text

    except:

        return "News unavailable right now."


def ai_answer(q):

    q=q.lower()

    if "blockchain" in q:

        return """🔗 Blockchain

Blockchain is a decentralized digital ledger that records transactions across many computers.

Each block contains:
• transaction data
• timestamp
• cryptographic hash

Once recorded, the data cannot be changed, making blockchain transparent and secure.

It powers cryptocurrencies like Bitcoin and Ethereum."""

    elif "bitcoin" in q:

        return """₿ Bitcoin

Bitcoin is the first decentralized cryptocurrency created in 2009 by Satoshi Nakamoto.

Key features:
• limited supply (21 million)
• decentralized network
• secure blockchain

Bitcoin is often called digital gold."""

    elif "ethereum" in q:

        return """Ξ Ethereum

Ethereum is a decentralized blockchain that supports smart contracts and decentralized applications.

It allows developers to build:
• DeFi platforms
• NFT marketplaces
• Web3 apps"""

    else:

        return "Ask me anything about crypto, trading or blockchain."


def updates(offset):

    try:
        r = requests.get(URL+"getUpdates",params={"offset":offset})
        return r.json()
    except:
        return {}


offset = 0

while True:

    data = updates(offset)

    if "result" not in data:
        time.sleep(1)
        continue

    for u in data.get("result",[]):

        offset = u["update_id"]+1

        if "message" not in u:
            continue

        msg = u["message"]

        if "text" not in msg:
            continue

        chat = msg["chat"]["id"]
        text = msg["text"].strip()


        if text == "/start":

            send(chat,
                 "🤖 Welcome to your Crypto AI Assistant\nChoose a menu:",
                 main_menu)


        elif "Learn" in text:

            send(chat,
"""📚 Crypto Education

Cryptocurrency is digital money secured by cryptography and powered by blockchain technology.

Blockchain is a decentralized ledger where transactions are recorded across many computers.

Advantages:
• transparency
• security
• decentralization
• global access

Cryptocurrencies remove intermediaries like banks.""",
            back_menu)


        elif "Trading" in text:

            send(chat,
"""📈 Trading

Crypto trading is buying and selling cryptocurrencies to profit from price movements.

Main strategies:

Scalping – very fast trades
Day trading – trades opened and closed same day
Swing trading – trades lasting days or weeks
Trend trading – following long market trends""",
            back_menu)


        elif "Risk" in text:

            send(chat,
"""⚠ Risk Management

Risk management protects your capital.

Golden rules:
• never risk more than 2% per trade
• always use stop loss
• diversify your portfolio
• avoid emotional trading""",
            back_menu)


        elif "Market" in text:

            send(chat,
"""📊 Market Cycles

Crypto markets move in cycles:

1️⃣ Accumulation
2️⃣ Uptrend
3️⃣ Distribution
4️⃣ Downtrend

Understanding cycles helps investors buy low and sell high.""",
            back_menu)


        elif "Price" in text:

            send(chat,"Choose a cryptocurrency:",price_menu)


        elif text=="BTC":

            p=price("bitcoin")
            send(chat,f"₿ Bitcoin price: ${p}")

        elif text=="ETH":

            p=price("ethereum")
            send(chat,f"Ξ Ethereum price: ${p}")

        elif text=="SOL":

            p=price("solana")
            send(chat,f"◎ Solana price: ${p}")

        elif text=="BNB":

            p=price("binancecoin")
            send(chat,f"BNB price: ${p}")


        elif "Charts" in text:

            send(chat,"Choose chart:",chart_menu)


        elif "BTC Chart" in text:

            send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT")

        elif "ETH Chart" in text:

            send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:ETHUSDT")

        elif "SOL Chart" in text:

            send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:SOLUSDT")

        elif "BNB Chart" in text:

            send(chat,"https://www.tradingview.com/chart/?symbol=BINANCE:BNBUSDT")


        elif "Altcoins" in text:

            send(chat,
"""🌕 Altcoins

Altcoins are cryptocurrencies other than Bitcoin.

Popular altcoins:
• Ethereum
• Solana
• Cardano
• Avalanche
• Polkadot""",
            back_menu)


        elif "Staking" in text:

            send(chat,
"""🔒 Staking

Staking means locking your crypto in a network to help validate transactions.

In return you receive rewards.

Popular staking coins:
• Ethereum
• Cardano
• Solana""",
            back_menu)


        elif "Portfolio" in text:

            send(chat,
"""💼 Portfolio Strategy

Example crypto portfolio:

50% Bitcoin
25% Ethereum
15% Altcoins
10% Stablecoins

Diversification reduces risk.""",
            back_menu)


        elif "News" in text:

            send(chat,crypto_news(),back_menu)


        elif "AI" in text:

            send(chat,"Ask any crypto question.",back_menu)


        elif "Back" in text:

            send(chat,"Main menu",main_menu)


        else:

            send(chat,ai_answer(text))


    time.sleep(1)
