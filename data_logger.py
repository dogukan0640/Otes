import pandas as pd, os, numpy as np
LOG_FILE = "signals.csv"

def log_signal(d: dict):
    new = pd.DataFrame([d])
    # sütunlar kesin dursun
    cols = ["timestamp","signal_id","symbol","interval","rsi","atr",
            "trend_direction","entry_price","tp","sl",
            "confidence_score","result"]
    if "result" not in new.columns:
        new["result"] = np.nan                         # her eklemede garanti
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        if "result" not in df.columns:                 # eski csv’de yoksa ekle
            df["result"] = np.nan
        df = pd.concat([df, new], ignore_index=True)
    else:
        df = new[cols]                                 # ilk kez oluştururken
    df.to_csv(LOG_FILE, index=False)
