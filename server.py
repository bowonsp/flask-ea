from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Ganti ini dengan API key kamu sendiri
openai.api_key = "YOUR_OPENAI_API_KEY"

@app.route('/')
def home():
    return 'AI Flask EA server is running.'

@app.route('/signal', methods=['POST'])
def signal():
    try:
        data = request.get_json()

        # Pastikan data yang dikirim valid
        if not data or 'symbol' not in data or 'timeframe' not in data or 'candles' not in data:
            return jsonify({"error": "Invalid request data"}), 400

        prompt = f"""
Symbol: {data['symbol']}
Timeframe: {data['timeframe']}
Candles: {data['candles']}

Berdasarkan data di atas dan menggunakan analisa EMA + Bollinger Bands, berikan sinyal BUY, SELL, atau HOLD. Sertakan juga SL dan TP.
Jawab hanya dalam format:
Action: BUY/SELL/HOLD
SL: <angka>
TP: <angka>
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=100
        )

        reply = response['choices'][0]['message']['content']
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
