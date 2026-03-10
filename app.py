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
["1️⃣ Learn","2️⃣ Trading"],
["3️⃣ Risk","4️⃣ Market"],
["5️⃣ Price","6️⃣ Charts"],
["7️⃣ Altcoins","8️⃣ Staking"],
["9️⃣ Portfolio","🔟 News"],
["1️⃣1️⃣ AI Assistant","🌐 Language"]
],
"resize_keyboard":True
}

# ===================== SEND FUNCTION =====================

def send(chat,text,menu=None):

    payload={
    "chat_id":chat,
    "text":text
    }

    if menu:
        payload["reply_markup"]=menu

    requests.post(URL+"/sendMessage",json=payload)

# ===================== WEBHOOK =====================

@app.route("/",methods=["GET"])
def home():
    return "Bot running"

@app.route(f"/{TOKEN}",methods=["POST"])
def bot():

    data=request.json

    if "message" in data:

        chat=data["message"]["chat"]["id"]
        text=data["message"].get("text","")

        if chat not in user_lang:
            user_lang[chat]="EN"

# ===================== PORTFOLIO =====================

        if text=="9️⃣ Portfolio":

            send(chat,
            "9️⃣ Portfolio Management\n\n"
            "Managing a portfolio involves tracking "
            "and balancing different crypto investments.",
            portfolio_menu)

        elif text=="9.1 Diversification":

            send(chat,"Diversification spreads assets.",portfolio_menu)

        elif text=="9.2 Long Term Investing":

            send(chat,"Long term investing focuses on future growth.",portfolio_menu)

        elif text=="9.3 Portfolio Tracking":

            send(chat,"Tracking helps measure performance.",portfolio_menu)

        elif text=="9.4 Rebalancing":

            send(chat,"Rebalancing adjusts portfolio allocations.",portfolio_menu)

# ===================== NEWS =====================

        elif text=="🔟 News":

            send(chat,
            "🔟 Crypto News Sources\n\n"
            "Select a news source to open the website.",
            news_menu)

        elif text=="10.1 CoinDesk":

            send(chat,"https://www.coindesk.com")

        elif text=="10.2 CoinTelegraph":

            send(chat,"https://cointelegraph.com")

        elif text=="10.3 Decrypt":

            send(chat,"https://decrypt.co")

        elif text=="10.4 Binance News":

            send(chat,"https://www.binance.com/en/news")

# ===================== AI =====================

        elif text=="1️⃣1️⃣ AI Assistant":

            ai_mode[chat]=True

            send(chat,
            "1️⃣1️⃣ AI Assistant\n\n"
            "Ask any cryptocurrency question.\n\n"
            "Press ⬅ Back to exit AI mode.")

# ===================== AI RESPONSE =====================

        elif chat in ai_mode and ai_mode[chat] and text not in [
        "⬅ Back",
        "1️⃣ Learn","2️⃣ Trading","3️⃣ Risk","4️⃣ Market",
        "5️⃣ Price","6️⃣ Charts","7️⃣ Altcoins","8️⃣ Staking",
        "9️⃣ Portfolio","🔟 News","🌐 Language"
        ]:

            try:

                r=requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                "Authorization":f"Bearer {GROQ_API_KEY}",
                "Content-Type":"application/json"
                },
                json={
                "model":"llama-3.3-70b-versatile",
                "messages":[
                {"role":"system","content":"You are a crypto expert assistant."},
                {"role":"user","content":text}
                ]
                })

                answer=r.json()["choices"][0]["message"]["content"]

                send(chat,answer)

            except:

                send(chat,"AI service unavailable.")

# ===================== BACK =====================

        elif text=="⬅ Back":

            ai_mode[chat]=False

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
