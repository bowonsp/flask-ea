from flask import Flask, request, jsonify
from strategy import generate_signal

app = Flask(__name__)

@app.route('/signal', methods=['POST'])
def signal():
    try:
        print("==> Signal endpoint hit")
        data = request.get_json()
        print(f"==> Received data: {data}")

        result = generate_signal(data)
        print(f"==> Signal result: {result}")

        return jsonify(result)
    except Exception as e:
        print(f"==> Error occurred: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
