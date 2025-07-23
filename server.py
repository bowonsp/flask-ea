from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Ganti dengan OpenAI API key kamu
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-xxx")  # Bisa diatur di Render as environment variable

@app.route("/")
def index():
    return "EA Flask Server is running."

@app.route("/signal", methods=["POST"])
def signal():
    try:
        data = request.get_json()
        if not data or "close" not in data:
            return jsonify({"error": "Invalid request. 'close' data missing."}), 400

        close = data["close"]
        prompt = (
            f"Berdasarkan data penutupan 10 candle terakhir: {close}, "
            f"berikan sinyal trading (BUY / SELL / HOLD) berdasarkan tren, EMA, dan Bollinger Bands. "
            f"Jawab dalam format JSON misalnya: {{\"signal\": \"BUY\", \"sl\": 1.12345, \"tp\": 1.12500}}"
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Kamu adalah analis trading profesional."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        ai_reply = response.choices[0].message["content"]

        # Coba parse hasil AI sebagai JSON (jika valid)
        try:
            import json
            parsed = json.loads(ai_reply)
            return jsonify(parsed)
        except Exception:
            return jsonify({"error": "AI response tidak dalam format JSON", "raw": ai_reply}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # agar bisa di-host di Render.com
    app.run(host="0.0.0.0", port=port)
