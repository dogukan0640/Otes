# ─── trade_result_watcher.py ─────────────────────────────────────────
import os, time, traceback, requests
import pandas as pd
import numpy as np

TOKEN = "7744478523:AAEtRJar6uF7m0cxKfQh7r7TltXYxWwtmm0"
CHAT  = "1009868232"
LOG   = "signals.csv"

def tg(msg):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                  data={"chat_id": CHAT, "text": msg})

def get_price(symbol: str) -> float:
    r = requests.get(f"https://api.binance.com/api/v3/ticker/price",
                     params={"symbol": symbol}, timeout=5)
    return float(r.json()["price"])

def watch():
    # csv yoksa sessizce çık
    if not os.path.exists(LOG):
        return

    df = pd.read_csv(LOG)

    # result sütunu eksikse ekle → bir sonraki döngüde devam
    if "result" not in df.columns:
        df["result"] = np.nan
        df.to_csv(LOG, index=False)
        return

    pending = df[df["result"].isna()].copy()
    if pending.empty:
        return

    changed = False
    for idx, row in pending.iterrows():
        p = get_price(row["symbol"])
        if p >= row["tp"]:             # TP
            df.at[idx, "result"] = 1
            tg(f"[TP] {row['signal_id']} {row['symbol']} hedefe ulaştı.")
            changed = True
        elif p <= row["sl"]:           # SL
            df.at[idx, "result"] = 0
            tg(f"[SL] {row['signal_id']} {row['symbol']} stop oldu.")
            changed = True
        time.sleep(0.1)                # API limiti

    if changed:
        df.to_csv(LOG, index=False)

if __name__ == "__main__":
    try:
        watch()
    except Exception:
        tg(f"[HATA] trade_result_watcher\n{traceback.format_exc()}")
        raise
# ─────────────────────────────────────────────────────────────────────
