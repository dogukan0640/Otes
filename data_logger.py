import pandas as pd
import os
from datetime import datetime

def log_signal(data_dict):
    log_file = "signals.csv"
    new_entry = pd.DataFrame([data_dict])

    if os.path.exists(log_file):
        existing = pd.read_csv(log_file)
        updated = pd.concat([existing, new_entry], ignore_index=True)
    else:
        updated = new_entry

    updated.to_csv(log_file, index=False)
    print(f"Sinyal loglandı: {data_dict['symbol']} - {data_dict['interval']}")

if __name__ == "__main__":
    sample_signal = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "symbol": "BTCUSDT",
        "interval": "15m",
        "rsi": 42.7,
        "atr": 80.5,
        "trend_direction": "up",
        "entry_price": 65000.0,
        "tp": 66000.0,
        "sl": 64500.0,
        "confidence_score": 76.5
    }
    log_signal(sample_signal)
