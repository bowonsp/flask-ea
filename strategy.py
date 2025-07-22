import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def predict_signal(data):
    price = data.get("price", 0)
    symbol = data.get("symbol", "")
    rsi = data.get("rsi", 50)

    prompt = f"""
    Symbol: {symbol}
    Price: {price}
    RSI: {rsi}
    
    Berdasarkan data di atas, apakah sinyal trading yang sesuai? Jawab hanya dengan: BUY, SELL, atau HOLD.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4",  # atau gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "Kamu adalah analis trading profesional."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )

        signal_text = response.choices[0].message.content.strip().upper()

        # Hitung TP/SL berdasarkan sinyal
        pip_size = 1 if price > 1000 else 0.0001  # misal BTC/USD vs EUR/USD
        if signal_text == "BUY":
            tp = price + 50 * pip_size
            sl = price - 50 * pip_size
        elif signal_text == "SELL":
            tp = price - 50 * pip_size
            sl = price + 50 * pip_size
        else:
            tp = sl = price

        return {
            "signal": signal_text,
            "tp": tp,
            "sl": sl
        }

    except Exception as e:
        return {
            "error": str(e),
            "signal": "HOLD",
            "tp": price,
            "sl": price
        }
