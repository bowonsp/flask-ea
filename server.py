from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from strategy import generate_signal

app = Flask(__name__)
CORS(app)  # <- penting

@app.route('/signal', methods=['POST'])
def signal():
    try:
        data = request.get_json(force=True)
        symbol = data.get("symbol")
        close_prices = data.get("close", [])

        if not symbol or not close_prices:
            return jsonify({"error": "Missing symbol or close data"}), 400

        result = generate_signal(close_prices)
        return jsonify({"signal": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
