from flask import Flask, request, jsonify
from strategy import generate_signal

app = Flask(__name__)

@app.route('/signal', methods=['POST'])
def signal():
    try:
        data = request.get_json(force=True)  # <- Fix penting di sini!
        symbol = data.get("symbol")
        close_prices = data.get("close", [])

        if not close_prices or not symbol:
            return jsonify({"error": "Missing data"}), 400

        signal = generate_signal(close_prices)
        return signal, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
