import os
import openai

# Ambil API key dari environment variable di Render
openai.api_key = os.getenv("OPENAI_API_KEY")

def predict_signal(data):
    price = data.get("price", 0)
    symbol = data.get("symbol", "")
    rsi = data.get("rsi", 50)

    prompt = f"""
    Pair: {symbol}
    Price: {price}
    RSI: {rsi}

    Berdasarkan data di atas, apa sinyal trading yang paling tepat?
    Jawab hanya dengan salah satu dari: BUY, SELL, atau HOLD.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # ganti ke "gpt-3.5-turbo" jika akun kamu tidak punya akses GPT-4
            messages=[
                {"role": "system", "content": "Kamu adalah analis teknikal profesional yang memberikan sinyal trading secara akurat."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )

        signal_text = response.choices[0].message.content.strip().upper()

        # Hitung TP/SL berdasarkan sinyal
        pip_size = 1 if price > 1000 else 0.0001  # BTCUSD pakai pip 1, forex pakai 0.0001
        if signal_text == "BUY":
            tp = price + 50 * pip_size
            sl = price - 50 * pip_size
        elif signal_text == "SELL":
            tp = price - 50 * pip_size
            sl = price + 50 * pip_size
        else:
            tp = price
            sl = price

        return {
            "signal": signal_text,
            "tp": round(tp, 5),
            "sl": round(sl, 5)
        }

    except Exception as e:
        return {
            "error": str(e),
            "signal": "HOLD",
            "tp": price,
            "sl": price
        }
