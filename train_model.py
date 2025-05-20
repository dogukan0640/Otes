import pandas as pd
import lightgbm as lgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import traceback, requests, os

TOKEN = "7744478523:AAEtRJar6uF7m0cxKfQh7r7TltXYxWwtmm0"
CHAT  = "1009868232"
def alert(msg):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                  data={"chat_id": CHAT, "text": msg})

MODEL_PATH = "model.pkl"

def train_lightgbm_model():
    df = pd.read_csv("signals_enriched.csv").dropna()

    # --- hedef kolonu oluştur ---
    if "confidence_score" in df.columns:
        df["target"] = (df["confidence_score"] > 70).astype(int)
    elif "güven_puanı" in df.columns:
        df["target"] = (df["güven_puanı"] > 70).astype(int)
    else:
        # etiket yok → hepsi 0
        df["target"] = 0

    features = ["rsi", "atr"]
    X = df[features]
    y = df["target"]

    # Eğitim- test böl
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2,
                                              random_state=42, stratify=y)

    model = lgb.LGBMClassifier()
    model.fit(X_tr, y_tr)

    acc = accuracy_score(y_te, model.predict(X_te))
    joblib.dump(model, MODEL_PATH)
    return acc

if __name__ == "__main__":
    try:
        acc = train_lightgbm_model()
        alert(f"[AI EĞİTİM] İlk model kaydedildi – doğruluk: {acc:.2f}")
    except Exception:
        alert(f"[HATA] train_model.py\n{traceback.format_exc()}")
        raise
