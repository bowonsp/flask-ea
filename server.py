
from flask import Flask, request, jsonify
from strategy import generate_signal

app = Flask(__name__)

@app.route('/signal', methods=['POST'])
def signal():
    data = request.get_json(force=True)
    try:
        symbol = data.get("symbol")
        close_prices = data.get("close", [])
        signal = generate_signal(close_prices)
        return signal, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
