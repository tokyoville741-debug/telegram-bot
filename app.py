import os
from flask import Flask, request
import asyncio
import requests
import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

# ================= BINANCE DATA =================

def get_klines(symbol="BTCUSDT", interval="15m", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    data = requests.get(url).json()

    df = pd.DataFrame(data, columns=[
        "time","open","high","low","close","volume",
        "close_time","qav","num_trades","taker_base_vol",
        "taker_quote_vol","ignore"
    ])

    df["close"] = df["close"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)

    return df

# ================= INDICATORS =================

def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# ================= SIGNAL =================

def generate_signal(symbol):

    df = get_klines(symbol)

    df["ema9"] = ema(df["close"], 9)
    df["ema21"] = ema(df["close"], 21)
    df["rsi"] = rsi(df["close"])

    last = df.iloc[-1]

    if last["ema9"] > last["ema21"] and last["rsi"] < 70:
        return f"{symbol} BUY signal"
    elif last["ema9"] < last["ema21"] and last["rsi"] > 30:
        return f"{symbol} SELL signal"
    else:
        return f"{symbol} NO SIGNAL"

# ================= TELEGRAM =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is running")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):

    symbol = "BTCUSDT"

    if context.args:
        symbol = context.args[0].upper()

    result = generate_signal(symbol)

    await update.message.reply_text(result)

# ================= BOT LOOP =================

def run_bot():

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("signal", signal))

    application.run_polling()

# ================= WEB SERVER =================

@app.route("/")
def home():
    return "Bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    return "ok"

# ================= MAIN =================

if __name__ == "__main__":

    from threading import Thread

    bot_thread = Thread(target=run_bot)
    bot_thread.start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
