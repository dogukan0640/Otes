# ⬇︎  train_model.py  (tam dosya)
import pandas as pd, numpy as np, lightgbm as lgb, joblib, os, requests, traceback
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

TOKEN, CHAT = "7744478523:AAEtRJar6uF7m0cxKfQh7r7TltXYxWwtmm0", "1009868232"
tg = lambda m: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                             data={"chat_id": CHAT, "text": m})

def train():
    if not os.path.exists("signals.csv"):
        tg("[AI] signals.csv yok, eğitim atlandı."); return
    df = pd.read_csv("signals.csv").dropna(subset=["result"])
    if df.empty:
        tg("[AI] Etiketli veri yok, eğitim atlandı."); return

    X = df[["rsi","atr"]].fillna(0)
    y = df["result"].astype(int)

    # ­­­ küçük veri kontrolü
    if len(y) < 2:                         # yalnızca 1 örnek
        dummy = lgb.LGBMClassifier()
        dummy.fit(X, y)
        joblib.dump(dummy, "model.pkl")
        tg("[AI] 1 örnekle geçici model kaydedildi.")
        return

    if len(y) < 5:                         # 2-4 örnek → tüm veriyi kullan
        model = lgb.LGBMClassifier()
        model.fit(X, y)
        joblib.dump(model, "model.pkl")
        tg(f"[AI] Küçük veriyle model kaydedildi (n={len(y)}).")
        return

    X_tr,X_te,y_tr,y_te = train_test_split(X,y,test_size=0.2,random_state=1,stratify=y)
    model = lgb.LGBMClassifier(class_weight="balanced")
    model.fit(X_tr, y_tr)
    acc = accuracy_score(y_te, model.predict(X_te))
    joblib.dump(model, "model.pkl")
    tg(f"[AI] Model kaydedildi – doğruluk: {acc:.2f}")

if __name__ == "__main__":
    try: train()
    except Exception:
        tg(f"[HATA] train_model.py\n{traceback.format_exc()}")
        raise
