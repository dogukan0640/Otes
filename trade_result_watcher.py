
import pandas as pd, numpy as np, requests, time, traceback

TOKEN = "7744478523:AAEtRJar6uF7m0cxKfQh7r7TltXYxWwtmm0"
CHAT  = "1009868232"
LOG   = "signals.csv"

def tg(msg): 
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                  data={"chat_id": CHAT, "text": msg})

def get_price(symbol:str)->float:
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    r = requests.get(url, timeout=5)
    return float(r.json()['price'])

def watch():
    try:
        df = pd.read_csv(LOG)
    except FileNotFoundError:
        return
    pending = df[df['result'].isna()].copy()
    if pending.empty:
        return
    updated = False
    for idx,row in pending.iterrows():
        sym = row['symbol']
        price = get_price(sym)
        # LONG varsayıyoruz
        if price >= row['tp']:
            df.loc[idx,'result']=1
            tg(f"[TP] {sym} ID {row['signal_id']} hedefe ulaştı.")
            updated=True
        elif price <= row['sl']:
            df.loc[idx,'result']=0
            tg(f"[SL] {sym} ID {row['signal_id']} stop oldu.")
            updated=True
        time.sleep(0.1)
    if updated:
        df.to_csv(LOG,index=False)

if __name__ == "__main__":
    try:
        watch()
    except Exception:
        tg(f"[HATA] trade_result_watcher\n{traceback.format_exc()}")
        raise
