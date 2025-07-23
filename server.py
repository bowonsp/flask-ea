from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/signal", methods=["POST"])
def signal():
    data = request.get_json(force=True, silent=True)
    if data is None:
        return jsonify({"error": "Invalid or no JSON received"}), 400

    # Debug log
    print("Received data:", data)

    symbol = data.get("symbol")
    timeframe = data.get("timeframe")
    close = data.get("close")

    if not symbol or not timeframe or not close:
        return jsonify({"error": "Missing fields"}), 400

    # Logika prediksi sederhana
    if close[-1] > close[-2]:
        return jsonify({"signal": "BUY"})
    elif close[-1] < close[-2]:
        return jsonify({"signal": "SELL"})
    else:
        return jsonify({"signal": "HOLD"})
