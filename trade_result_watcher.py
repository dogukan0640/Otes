import pandas as pd, numpy as np, requests, time, traceback

TOKEN = "7744478523:AAEtRJar6uF7m0cxKfQh7r7TltXYxWwtmm0"
CHAT  = "1009868232"
LOG   = "signals.csv"

def tg(m): requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                         data={"chat_id": CHAT, "text": m})

def get_price(sym):   # basit fiyat sorgusu
    r = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={sym}",
                     timeout=5)
    return float(r.json()["price"])

def watch():
    if not os.path.exists(LOG): return
    df = pd.read_csv(LOG)
    if "result" not in df.columns:        # <─ hataya düşen kısım
        df["result"] = np.nan
        df.to_csv(LOG,index=False)
        return                            # sonraki döngüde işlemeye devam

    pending = df[df["result"].isna()].copy()
    if pending.empty: return

    changed = False
    for idx,row in pending.iterrows():
        p = get_price(row["symbol"])
        if p >= row["tp"]:
            df.at[idx,"result"]=1
            tg(f"[TP] {row['signal_id']} {row['symbol']} hedefe ulaştı.")
            changed=True
        elif p <= row["sl"]:
            df.at[idx,"result"]=0
            tg(f"[SL] {row['signal_id']} {row['symbol']} stop oldu.")
            changed=True
        time.sleep(0.1)

    if changed: df.to_csv(LOG,index=False)

if __name__ == "__main__":
    try: watch()
    except Exception: 
        tg(f"[HATA] trade_result_watcher\\n{traceback.format_exc()}")
        raise
