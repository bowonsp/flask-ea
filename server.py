from flask import Flask, request, jsonify
from strategi import generate_signal

app = Flask(__name__)

@app.route("/")
def home():
    return "OpenAI Signal Server is Running"

@app.route("/signal", methods=["POST"])
def signal():
    try:
        data = request.get_json()
        if not data or 'candles' not in data:
            return jsonify({"error": "Invalid payload"}), 400

        signal_result = generate_signal(data)
        return jsonify(signal_result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
