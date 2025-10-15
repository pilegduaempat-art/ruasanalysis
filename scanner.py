import ccxt
import pandas as pd
import numpy as np
from utils import calculate_volatility, fear_greed_index, whale_bias

exchange = ccxt.binance({
    'enableRateLimit': True,
    'options': {'defaultType': 'future'}
})

def fetch_futures_data(limit=50):
    tickers = exchange.fetch_tickers()
    futures = {k: v for k, v in tickers.items() if 'USDT' in k and 'PERP' in k}
    
    data = []
    for symbol, info in list(futures.items())[:limit]:
        try:
            price = info['last']
            change_24h = info['percentage']
            volume = info['quoteVolume']
            ohlcv = exchange.fetch_ohlcv(symbol, '1h', limit=100)
            df = pd.DataFrame(ohlcv, columns=['time','open','high','low','close','volume'])
            vol_index = calculate_volatility(df['close'])
            volume_change = (df['volume'].iloc[-1] - df['volume'].mean()) / df['volume'].mean()

            ob = exchange.fetch_order_book(symbol)
            bias = whale_bias(ob)
            fg = fear_greed_index(vol_index, volume_change)

            data.append({
                'Symbol': symbol,
                'Price': price,
                '% Change (24H)': change_24h,
                'Volume 24H (USDT)': volume,
                'Volatility Index': round(vol_index, 2),
                'Whale Bias': bias,
                'Fear & Greed': round(fg, 1)
            })
        except Exception:
            continue

    df = pd.DataFrame(data)
    df['Rank Volatile'] = df['Volatility Index'].rank(ascending=False)
    return df.sort_values(by='Volatility Index', ascending=False)
