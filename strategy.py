def generate_signal(data):
    candles = data.get("candles", [])
    if len(candles) < 2:
        return {"signal": "HOLD"}

    last_close = candles[-1]["close"]
    prev_close = candles[-2]["close"]

    if last_close > prev_close:
        return {"signal": "BUY", "tp": last_close + 10, "sl": last_close - 10}
    elif last_close < prev_close:
        return {"signal": "SELL", "tp": last_close - 10, "sl": last_close + 10}
    else:
        return {"signal": "HOLD"}
