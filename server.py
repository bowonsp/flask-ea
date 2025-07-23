from flask import Flask, request, jsonify
import openai
import os

# Inisialisasi Flask dan OpenAI
app = Flask(__name__)
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise RuntimeError("OPENAI_API_KEY tidak ditemukan di environment variables.")

client = openai.OpenAI(api_key=openai_api_key)

# Fungsi bantu buat prompt dari data candle
def build_prompt(data):
    close_prices = data.get("close", [])
    symbol = data.get("symbol", "UNKNOWN")
    timeframe = data.get("timeframe", "M1")
    
    prompt = (
        f"Analisis sinyal trading berdasarkan data harga penutupan berikut untuk {symbol} timeframe {timeframe}:\n"
        f"{close_prices}\n\n"
        "Berdasarkan data ini, apakah sinyal trading saat ini adalah BUY, SELL, atau HOLD? "
        "Jawab hanya dengan salah satu: BUY, SELL, atau HOLD."
    )
    return prompt

@app.route("/signal", methods=["POST"])
def signal():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Data JSON tidak valid"}), 400

        prompt = build_prompt(data)

        # Kirim ke OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Kamu adalah asisten trading."},
                {"role": "user", "content": prompt}
            ]
        )

        ai_reply = response.choices[0].message.content.strip().upper()

        # Validasi respons
        if ai_reply not in ["BUY", "SELL", "HOLD"]:
            return jsonify({"signal": "HOLD", "note": "Respons AI tidak dikenali: " + ai_reply}), 200

        return jsonify({"signal": ai_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
