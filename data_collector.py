import requests
import pandas as pd
import time
from datetime import datetime

BINANCE_API = "https://api.binance.com/api/v3/klines"
TIMEFRAMES = ['1w', '1d', '4h', '1h', '15m', '5m']
LIMIT = 200

def get_symbols():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)
    symbols = []
    if response.status_code == 200:
        data = response.json()
        for symbol_info in data['symbols']:
            if symbol_info['quoteAsset'] == 'USDT' and symbol_info['status'] == 'TRADING':
                symbols.append(symbol_info['symbol'])
    return symbols

def fetch_klines(symbol, interval, limit):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(BINANCE_API, params=params)
    if response.status_code == 200:
        raw_data = response.json()
        df = pd.DataFrame(raw_data, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
        ])
        df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
        df['symbol'] = symbol
        df['interval'] = interval
        return df
    else:
        print(f"Error fetching {symbol} - {interval}: {response.text}")
        return pd.DataFrame()

def collect_all_data():
    all_data = []
    symbols = get_symbols()
    print(f"Toplam {len(symbols)} sembol bulundu.")
    for symbol in symbols:
        for tf in TIMEFRAMES:
            df = fetch_klines(symbol, tf, LIMIT)
            if not df.empty:
                all_data.append(df)
            time.sleep(0.1)
    combined = pd.concat(all_data, ignore_index=True)
    return combined

if __name__ == "__main__":
    df = collect_all_data()
    df.to_csv("signals.csv", index=False)
    print("Veri toplama tamamlandı ve signals.csv oluşturuldu.")
