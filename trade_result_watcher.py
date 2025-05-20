
import os, pandas as pd, numpy as np, requests, time, traceback

TOKEN="7744478523:AAEtRJar6uF7m0cxKfQh7r7TltXYxWwtmm0"
CHAT="1009868232"
LOG="signals.csv"
def tg(m): requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                         data={"chat_id":CHAT,"text":m})
def price(sym):
    r=requests.get("https://api.binance.com/api/v3/ticker/price",params={"symbol":sym},timeout=5)
    return float(r.json()["price"])
def watch():
    if not os.path.exists(LOG): return
    df=pd.read_csv(LOG)
    for col in ["tp","sl","result"]:
        if col not in df.columns:
            df[col]=np.nan
    pending=df[df["result"].isna()].copy()
    if pending.empty:
        df.to_csv(LOG,index=False); return
    changed=False
    for idx,row in pending.iterrows():
        p=price(row["symbol"])
        if not np.isnan(row["tp"]) and p>=row["tp"]:
            df.at[idx,"result"]=1; tg(f"[TP] {row['signal_id']}")
            changed=True
        elif not np.isnan(row["sl"]) and p<=row["sl"]:
            df.at[idx,"result"]=0; tg(f"[SL] {row['signal_id']}")
            changed=True
        time.sleep(0.1)
    if changed: df.to_csv(LOG,index=False)

if __name__=="__main__":
    try: watch()
    except Exception:
        tg(f"[HATA] trade_result_watcher\n{traceback.format_exc()}")
        raise
