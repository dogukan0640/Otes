# ─── train_model.py  (tamamen yenisi) ───────────────────────────
import pandas as pd, numpy as np, lightgbm as lgb, joblib, os, requests, traceback
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

TOKEN = "7744478523:AAEtRJar6uF7m0cxKfQh7r7TltXYxWwtmm0"
CHAT  = "1009868232"
tg = lambda m: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                             data={"chat_id": CHAT, "text": m})

def train():
    if not os.path.exists("signals.csv"):
        tg("[AI] signals.csv yok, eğitim atlandı."); return

    df = pd.read_csv("signals.csv").dropna(subset=["result"])
    if df.empty:
        tg("[AI] Etiketli veri yok, eğitim atlandı."); return

    X = df[["rsi", "atr"]].fillna(0)
    y = df["result"].astype(int)

    n = len(y)
    model = lgb.LGBMClassifier(class_weight="balanced")

    # — Küçük veri kuralı —
    if n < 5:
        model.fit(X, y)
        joblib.dump(model, "model.pkl")
        tg(f"[AI] {n} örnekle geçici model kaydedildi.")
        return

    # — Normal eğitim —
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, random_state=1, stratify=y
    )
    model.fit(X_tr, y_tr)
    acc = accuracy_score(y_te, model.predict(X_te))
    joblib.dump(model, "model.pkl")
    tg(f"[AI] Model kaydedildi – doğruluk: {acc:.2f}")

if __name__ == "__main__":
    try:
        train()
    except Exception:
        tg(f"[HATA] train_model.py\n{traceback.format_exc()}")
        raise
# ────────────────────────────────────────────────────────────────
