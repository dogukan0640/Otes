
import pandas as pd, numpy as np

cols = ["timestamp","signal_id","symbol","interval",
        "rsi","atr","trend_direction",
        "entry_price","tp","sl",
        "confidence_score","result"]
pd.DataFrame(columns=cols).to_csv("signals.csv", index=False)
print("signals.csv skeleton created with columns:", cols)
