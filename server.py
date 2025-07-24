from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai
import traceback

app = Flask(__name__)
CORS(app)

# OPENAI API KEY dari ENVIRONMENT VARIABLE
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return "Flask server is running."

@app.route('/signal', methods=['POST'])
def signal():
    try:
        data = request.get_json(force=True)
    except Exception as e:
        print("JSON decode error:", str(e))
        return jsonify({'error': f'Invalid JSON. {str(e)}'}), 400

    print("Data diterima:", data)

    close_prices = data.get('close', [])
    symbol = data.get('symbol', 'Unknown')
    timeframe = data.get('timeframe', 'Unknown')

    if not close_prices:
        return jsonify({'error': 'Data close kosong atau tidak ditemukan'}), 400

    # ==== PILIH MODE: LOGIKA SEDERHANA ATAU AI ====
    USE_SIMPLE_LOGIC = False  # Ubah ke True jika ingin non-AI (hanya BUY/SELL/HOLD sederhana)

    try:
        if USE_SIMPLE_LOGIC:
            # Logika sinyal sederhana
            if close_prices[-1] > close_prices[0]:
                signal_text = "BUY"
            elif close_prices[-1] < close_prices[0]:
                signal_text = "SELL"
            else:
                signal_text = "HOLD"

            print("Sinyal (logika sederhana):", signal_text)
            return jsonify({'signal': signal_text})

        else:
            # === AI ANALYSIS ===
            prompt = f"""
Berdasarkan data harga penutupan terakhir berikut ini untuk {symbol} ({timeframe}):
{close_prices}

Analisa arah pergerakan harga dan beri sinyal trading singkat:
BUY, SELL, atau HOLD. Hanya jawab sinyal tersebut.
"""

            print("Prompt untuk AI:", prompt.strip())

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )

            reply = response['choices'][0]['message']['content']
            print("AI response:", reply)

            return jsonify({"signal": reply.strip()})

    except Exception as e:
        error_msg = traceback.format_exc()
        print("ERROR DETAIL:\n", error_msg)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
