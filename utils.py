import numpy as np
import pandas as pd

def calculate_atr(high, low, close, period=14):
    tr = np.maximum(high - low, np.maximum(abs(high - close.shift()), abs(low - close.shift())))
    atr = tr.rolling(period).mean()
    return atr

def calculate_volatility(price_series):
    return np.std(price_series.pct_change()) * np.sqrt(1440) * 100  # annualized %

def normalize(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val + 1e-9)

def fear_greed_index(volatility, volume_change, funding_rate=0):
    vol_norm = normalize(volatility, 0, 100)
    volchg_norm = normalize(volume_change, -1, 1)
    fund_norm = normalize(funding_rate, -0.01, 0.01)
    score = (vol_norm + volchg_norm + fund_norm) / 3 * 100
    return np.clip(score, 0, 100)

def whale_bias(orderbook):
    bids = sum([b[1] for b in orderbook['bids']])
    asks = sum([a[1] for a in orderbook['asks']])
    bias = (bids - asks) / (bids + asks)
    if bias > 0.1:
        return f"🟩 Bullish ({bias:.1%})"
    elif bias < -0.1:
        return f"🟥 Bearish ({bias:.1%})"
    else:
        return f"⚪ Neutral ({bias:.1%})"
