# server.py

from flask import Flask, request, jsonify
from strategy import predict_signal
import logging
from datetime import datetime

app = Flask(__name__)

# Logging ke file untuk debugging
logging.basicConfig(filename="ea_api.log", level=logging.INFO)

@app.route('/ai-signal', methods=['POST'])
def ai_signal():
    try:
        data = request.get_json()
        logging.info(f"[{datetime.now()}] Received: {data}")

        # Prediksi sinyal
        result = predict_signal(data)

        return jsonify(result)

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
