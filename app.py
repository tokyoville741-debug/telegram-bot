from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# ==============================
# CONFIGURATION
# ==============================

# Mets ta clé API OpenAI ici
OPENAI_API_KEY = "TA_CLE_API_OPENAI_ICI"

client = OpenAI(api_key=OPENAI_API_KEY)

# ==============================
# PAGE TEST
# ==============================

@app.route("/", methods=["GET"])
def home():
    return "Bot IA actif et fonctionnel 🚀"


# ==============================
# ROUTE PRINCIPALE DU BOT
# ==============================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.json
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "Aucun message reçu"}), 400

    try:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un assistant intelligent, utile et précis."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=500
        )

        reply = response.choices[0].message.content

        return jsonify({
            "reply": reply
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })


# ==============================
# LANCEMENT DU SERVEUR
# ==============================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
