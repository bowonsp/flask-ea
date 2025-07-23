from flask import Flask, request, jsonify
from strategi import generate_signal

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return '✅ Flask EA Signal Server is running!'

@app.route('/signal', methods=['POST'])
def signal():
    try:
        # Ambil data dari EA
        data = request.get_json(force=True)
        print("📥 Data diterima dari EA:", data)

        # Validasi input
        if not data or 'symbol' not in data or 'timeframe' not in data or 'candles' not in data:
            print("❌ Format data tidak valid")
            return jsonify({"error": "Invalid request format"}), 400

        # Panggil fungsi strategi AI
        signal_result = generate_signal(data)
        print("📤 Sinyal dikirim ke EA:", signal_result)

        return jsonify(signal_result)

    except Exception as e:
        import traceback
        print("🔥 ERROR INTERNAL SERVER 🔥")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
