from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def generate_signal(close_prices):
    if len(close_prices) < 10:
        return "HOLD"

    # Logika sederhana: harga terakhir vs rata-rata 5 candle
    last = close_prices[-1]
    avg = sum(close_prices[-5:]) / 5

    if last > avg:
        return "BUY"
    elif last < avg:
        return "SELL"
    else:
        return "HOLD"

@app.route("/")
def home():
    return "🚀 Flask EA server is running."

@app.route("/signal", methods=["POST"])
def signal():
    try:
        data = request.get_json()

        symbol = data.get("symbol")
        timeframe = data.get("timeframe")
        close = data.get("close")

        if not symbol or not timeframe or not close:
            return jsonify({"error": "Missing required fields: symbol, timeframe, or close"}), 400

        signal = generate_signal(close)
        return jsonify({"signal": signal})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # Gunakan port 10000 agar sesuai Render
