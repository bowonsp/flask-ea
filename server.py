# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai

app = Flask(__name__)
CORS(app)

# OpenAI API Key dari environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return "Flask server is running."

@app.route('/signal', methods=['POST'])
def signal():
    try:
        data = request.get_json(force=True)
        print("Data diterima:", data)

        close_prices = data.get('close', [])
        symbol = data.get('symbol', 'Unknown')
        timeframe = data.get('timeframe', 'Unknown')

        if not close_prices:
            return jsonify({'error': 'Data close kosong atau tidak ditemukan'}), 400

        # Logika sinyal sederhana
        if close_prices[-1] > close_prices[0]:
            signal = "BUY"
        elif close_prices[-1] < close_prices[0]:
            signal = "SELL"
        else:
            signal = "HOLD"

        print("Sinyal sementara:", signal)

        # Prompt untuk AI
        prompt = f"""
        Berdasarkan data harga penutupan terakhir berikut ini untuk {symbol} ({timeframe}):
        {close_prices}

        Analisa arah pergerakan harga dan beri sinyal trading singkat:
        BUY, SELL, atau HOLD. Hanya jawab sinyal tersebut.
        """

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        reply = response.choices[0].message.content.strip()
        print("AI response:", reply)

        return jsonify({"signal": reply})

    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print("ERROR DETAIL:\n", error_msg)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
