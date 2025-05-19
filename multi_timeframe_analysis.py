import pandas as pd
import numpy as np

def calculate_trend_direction(df):
    df['close'] = pd.to_numeric(df['close'])
    df['trend'] = df['close'].rolling(window=20).mean()
    df['trend_direction'] = np.where(df['close'] > df['trend'], 'up', 'down')
    return df

def calculate_rsi(df, period=14):
    df['close'] = pd.to_numeric(df['close'])
    delta = df['close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    df['rsi'] = rsi
    return df

def calculate_atr(df, period=14):
    df['high'] = pd.to_numeric(df['high'])
    df['low'] = pd.to_numeric(df['low'])
    df['close'] = pd.to_numeric(df['close'])
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    tr = np.maximum(high_low, np.maximum(high_close, low_close))
    df['atr'] = pd.Series(tr).rolling(window=period).mean()
    return df

def enrich_features(df):
    df = calculate_trend_direction(df)
    df = calculate_rsi(df)
    df = calculate_atr(df)
    return df

def process_all():
    df = pd.read_csv("signals.csv")
    results = []
    grouped = df.groupby(['symbol', 'interval'])
    for (symbol, interval), group in grouped:
        group = enrich_features(group)
        results.append(group)
    final_df = pd.concat(results, ignore_index=True)
    final_df.to_csv("signals_enriched.csv", index=False)
    print("Zaman dilimi analizleri tamamlandı ve signals_enriched.csv oluşturuldu.")

if __name__ == "__main__":
    process_all()
