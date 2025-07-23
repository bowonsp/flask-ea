from flask import Flask, request, jsonify
from strategy import generate_signal

app = Flask(__name__)

@app.route('/signal', methods=['POST'])
def signal():
    try:
        data = request.get_json(force=True)  # Paksa baca JSON
        symbol = data.get("symbol")
        close_prices = data.get("close", [])

        if not symbol or not close_prices:
            return jsonify({"error": "Missing symbol or close data"}), 400

        result = generate_signal(close_prices)

        return jsonify({"signal": result}), 200  # <- Fix di sini!
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
