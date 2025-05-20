
import pandas as pd, lightgbm as lgb, joblib, traceback, requests, os
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

TOKEN="7744478523:AAEtRJar6uF7m0cxKfQh7r7TltXYxWwtmm0"
CHAT="1009868232"
def tg(m): requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                         data={"chat_id": CHAT, "text": m})

def train():
    if not os.path.exists("signals.csv"):
        tg("[AI] signals.csv yok, eğitim atlandı.")
        return
    df = pd.read_csv("signals.csv")
    if "result" not in df.columns or df["result"].dropna().empty:
        tg("[AI] Etiketli veri yok, eğitim atlandı.")
        return
    df = df.dropna(subset=["result"])
    X = df[["rsi","atr"]].fillna(0)
    y = df["result"].astype(int)
    X_tr,X_te,y_tr,y_te = train_test_split(X,y,test_size=0.2,random_state=1,stratify=y)
    model = lgb.LGBMClassifier(class_weight="balanced")
    model.fit(X_tr,y_tr)
    acc = accuracy_score(y_te, model.predict(X_te))
    joblib.dump(model,"model.pkl")
    tg(f"[AI] Model kaydedildi – doğruluk: {acc:.2f}")

if __name__=="__main__":
    try: train()
    except Exception:
        tg(f"[HATA] train_model.py\n{traceback.format_exc()}")
        raise
