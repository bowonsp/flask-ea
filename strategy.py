import openai
import os
import json

# Ambil API key dari environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def predict_signal(data):
    """
    Kirim data ke OpenAI GPT dan dapatkan sinyal trading.
    """

    price = data.get("price", 0)
    symbol = data.get("symbol", "")
    rsi = data.get("rsi", 50)

    prompt = f"""
Saya adalah asisten trading. Berikut ini adalah data terbaru:

- Symbol: {symbol}
- Harga: {price}
- RSI: {rsi}

Berdasarkan data tersebut, apakah sebaiknya BUY, SELL, atau HOLD?
Berikan juga nilai TP dan SL yang wajar dalam format JSON seperti ini:

{{
  "signal": "BUY" atau "SELL" atau "HOLD",
  "tp": float,
  "sl": float
}}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # atau gpt-3.5-turbo kalau kamu pakai versi gratisan
            messages=[
                {"role": "system", "content": "Kamu adalah analis trading profesional. Jawaban harus dalam format JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        result_text = response['choices'][0]['message']['content']

        # Coba parsing JSON
        result = json.loads(result_text)

        return result

    except Exception as e:
        return {
            "signal": "HOLD",
            "tp": price,
            "sl": price,
            "error": str(e)
        }
