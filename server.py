from flask import Flask, request, jsonify
import openai
import os
import traceback  # Tambah ini

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/signal', methods=['POST'])
def signal():
    try:
        data = request.get_json(force=True)
        closes = data.get("close", [])

        if not closes:
            return jsonify({"error": "Missing close data"}), 400

        prompt = f"Beri sinyal BUY / SELL / HOLD berdasarkan data close berikut: {closes}"

        response = openai.chat.completions.create(  # ✅ API format baru
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Kamu adalah analis teknikal trading."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=20
        )

        signal = response.choices[0].message.content.strip()
        return jsonify({"signal": signal})

    except Exception as e:
        print("==== ERROR SERVER ====")
        print(e)
        traceback.print_exc()  # ✅ Tambah log lengkap di server
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host='0.0.0.0', port=port)
