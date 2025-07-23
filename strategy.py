# strategy.py

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def predict_signal(data):
    """
    Fungsi ini mengirim data indikator teknikal ke OpenAI dan mengembalikan sinyal trading.
    """
    try:
        symbol = data.get("symbol", "")
        price = data.get("price", 0)
        rsi = data.get("rsi", 0)
        ema = data.get("ema", 0)
        bb_upper = data.get("bb_upper", 0)
        bb_lower = data.get("bb_lower", 0)
        ema_period = data.get("ema_period", 14)
        bb_period = data.get("bb_period", 20)

        prompt = f"""
Pasangan: {symbol}
Harga Saat Ini: {price}
RSI: {rsi}
EMA({ema_period}): {ema}
Bollinger Bands({bb_period}): Upper={bb_upper}, Lower={bb_lower}

Berdasarkan data teknikal di atas, beri sinyal trading dalam format JSON seperti berikut:
{{
  \"signal\": \"BUY/SELL/HOLD\",
  \"tp\": <Take Profit>,
  \"sl\": <Stop Loss>
}}
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        # Parsing response
        reply = response.choices[0].message.content.strip()

        signal = "HOLD"
        tp = price
        sl = price

        if '"signal"' in reply:
            signal = reply.split('"signal"')[1].split('"')[1].upper()
        if '"tp"' in reply:
            tp = float(reply.split('"tp"')[1].split(',')[0].strip(": ").replace("}", ""))
        if '"sl"' in reply:
            sl = float(reply.split('"sl"')[1].split('}')[0].strip(": "))

        return {
            "signal": signal,
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
