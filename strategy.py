def generate_signal(data):
    candles = data['candles']

    if len(candles) < 2:
        return {'signal': 'HOLD'}

    last_close = candles[-1]['close']
    prev_close = candles[-2]['close']

    if last_close > prev_close:
        return {'signal': 'BUY'}
    elif last_close < prev_close:
        return {'signal': 'SELL'}
    else:
        return {'signal': 'HOLD'}
