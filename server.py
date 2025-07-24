import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

@app.route('/signal', methods=['POST'])
def signal():
    try:
        data = request.get_json(force=True)  # <= WAJIB pakai force=True
        print("Data diterima dari EA:", data)
        close_prices = data.get('close', [])
        symbol = data.get('symbol', 'UNKNOWN')
        timeframe = data.get('timeframe', 'UNKNOWN')

        if not close_prices or len(close_prices) < 2:
            return jsonify({"error": "Invalid close prices"}), 400

        prompt = (
            f"Berikan sinyal trading BUY, SELL, atau HOLD berdasarkan tren dari data close berikut:\n"
            f"{close_prices}\n\n"
            f"Jawaban satu kata saja, tanpa penjelasan."
        )

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=5
        )

        ai_reply = response.choices[0].message.content.strip().upper()
        # Filter hanya BUY/SELL/HOLD
        if ai_reply not in ["BUY", "SELL", "HOLD"]:
            ai_reply = "HOLD"

        return jsonify({"signal": ai_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
