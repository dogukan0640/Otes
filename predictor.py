
import pandas as pd, numpy as np, joblib, requests, uuid, time, traceback, os, data_logger

MODEL="model.pkl"
TOKEN="7744478523:AAEtRJar6uF7m0cxKfQh7r7TltXYxWwtmm0"
CHAT="1009868232"
def tg(m): requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                         data={"chat_id":CHAT,"text":m})

def predict():
    if not os.path.exists(MODEL):
        tg("[BOT] model.pkl bulunamadı.")
        return
    if not os.path.exists("signals_enriched.csv"):
        tg("[BOT] enriched veri yok.")
        return
    model = joblib.load(MODEL)
    df = pd.read_csv("signals_enriched.csv").dropna()
    X = df[["rsi","atr"]]
    df["ai_confidence"] = model.predict_proba(X)[:,1]*100
    strong = df[df["ai_confidence"]>=70]
    if strong.empty:
        tg("[BOT] Güçlü sinyal bulunamadı.")
        return
    for _,row in strong.iterrows():
        sig_id = f"{row['symbol']}-{int(time.time())}-{uuid.uuid4().hex[:4]}"
        entry = row["close"]
        tp = entry + row["atr"]
        sl = entry - row["atr"]*0.5
        msg = (f"[AI Sinyal] {row['symbol']} {row['interval']}\n"
               f"Entry {entry:.4f} TP {tp:.4f} SL {sl:.4f}\n"
               f"Güven {row['ai_confidence']:.1f}%\nID {sig_id}")
        tg(msg)
        data_logger.log_signal({
            "timestamp": row["open_time"],
            "signal_id": sig_id,
            "symbol": row["symbol"],
            "interval": row["interval"],
            "rsi": row["rsi"],
            "atr": row["atr"],
            "trend_direction": row["trend_direction"],
            "entry_price": entry,
            "tp": tp,
            "sl": sl,
            "confidence_score": row["ai_confidence"],
            "result": np.nan
        })

if __name__=="__main__":
    try: predict()
    except Exception:
        tg(f"[HATA] predictor.py\n{traceback.format_exc()}")
        raise
