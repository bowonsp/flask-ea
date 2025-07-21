# strategy.py

def predict_signal(data):
    """
    Fungsi ini bisa diganti pakai ML model di masa depan.
    Sekarang hanya aturan sederhana berdasarkan harga.
    """

    price = data.get("price", 0)
    symbol = data.get("symbol", "")
    
    if price < 70000:
        signal = "BUY"
    else:
        signal = "SELL"

    tp = price + 1000
    sl = price - 1000

    return {
        "signal": signal,
        "tp": tp,
        "sl": sl
    }
