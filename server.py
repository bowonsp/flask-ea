from flask import Flask, request, jsonify
from strategy import generate_signal
import traceback

app = Flask(__name__)

@app.route('/signal', methods=['POST'])
def signal():
    try:
        print("==> /signal endpoint hit")
        data = request.get_json()
        print(f"==> Received data: {data}")
        
        result = generate_signal(data)
        print(f"==> Result: {result}")

        return jsonify(result)
    except Exception as e:
        print("==> ERROR:")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
