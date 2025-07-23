from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Ganti dengan API key kamu di Render (pakai secret environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/signal", methods=["POST"])
def signal():
    try:
        data = request.get_json()

        symbol = data.get("symbol", "Unknown")
        timeframe = data.get("timeframe", "Unknown")
        close = data.get("close", [])

        if not close or not isinstance(close, list):
            return jsonify({"error": "Invalid or missing 'close' data"}), 400

        prompt = f"""
Data candle terakhir:
Symbol: {symbol}, Timeframe: {timeframe}
Close prices: {close}

Berdasarkan data ini dan indikator teknikal seperti Bollinger Bands dan EMA, beri sinyal BUY, SELL, atau HOLD.
Jawaban hanya boleh 1 kata (BUY, SELL, atau HOLD).
"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # atau "gpt-4" jika kamu pakai GPT-4
            messages=[
                {"role": "system", "content": "Kamu adalah analis trading profesional."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=10
        )

        reply = response["choices"][0]["message"]["content"].strip().upper()

        if reply not in ["BUY", "SELL", "HOLD"]:
            reply = "HOLD"

        return jsonify({"signal": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Untuk Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
