
import pandas as pd, numpy as np, os

LOG_FILE = "signals.csv"
COLS = ["timestamp","signal_id","symbol","interval",
        "rsi","atr","trend_direction",
        "entry_price","tp","sl",
        "confidence_score","result"]

def log_signal(d: dict):
    new = pd.DataFrame([d])
    for col in COLS:
        if col not in new.columns:
            new[col] = np.nan
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        for col in COLS:
            if col not in df.columns:
                df[col] = np.nan
        df = pd.concat([df, new[COLS]], ignore_index=True)
    else:
        df = new[COLS]
    df.to_csv(LOG_FILE, index=False)
