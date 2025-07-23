
def generate_signal(close_prices):
    if len(close_prices) < 10:
        return "HOLD"

    last = close_prices[-1]
    avg = sum(close_prices[-5:]) / 5

    if last > avg:
        return "BUY"
    elif last < avg:
        return "SELL"
    else:
        return "HOLD"
