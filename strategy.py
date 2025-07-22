# strategy.py

def predict_signal(data):
    """
    Fungsi ini bisa diganti pakai ML model di masa depan.
    Sekarang hanya aturan sederhana berdasarkan harga.
    """

    price = data.get("price", 0)
    symbol = data.get("symbol", "")
    
    if rsi < 30:
    signal = "BUY"
elif rsi > 70:
    signal = "SELL"
else:
    signal = "HOLD"

# Atur TP/SL dalam pip (contoh: 50 pip = 0.0050)
pip_size = 0.0001  # Untuk EURUSD
tp = price + (50 * pip_size) if signal == "BUY" else price - (50 * pip_size)
sl = price - (50 * pip_size) if signal == "BUY" else price + (50 * pip_size)


    return {
        "signal": signal,
        "tp": tp,
        "sl": sl
    }
