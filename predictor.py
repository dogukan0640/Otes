import pandas as pd
import joblib
import requests

MODEL_PATH = "model.pkl"
TELEGRAM_TOKEN = "7744478523:AAEtRJar6uF7m0cxKfQh7r7TltXYxWwtmm0"
CHAT_ID = "1009868232"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

def predict_and_notify():
    model = joblib.load(MODEL_PATH)
    df = pd.read_csv("signals_enriched.csv")
    df = df.dropna()

    features = ['rsi', 'atr']
    X = df[features]
    preds = model.predict_proba(X)[:, 1] * 100
    df['ai_confidence'] = preds

    strong_signals = df[df['ai_confidence'] >= 70]

    if strong_signals.empty:
        send_telegram_message("[BOT] Güçlü bir sinyal bulunamadı.")
    else:
        for _, row in strong_signals.iterrows():
            msg = (
                f"[AI Sinyal] {row['symbol']} - {row['interval']}
"
                f"RSI: {row['rsi']:.2f}, ATR: {row['atr']:.2f}
"
                f"Trend: {row['trend_direction']}
"
                f"Giriş: {row['entry_price']}, TP: {row['tp']}, SL: {row['sl']}
"
                f"AI Güven Skoru: {row['ai_confidence']:.2f}%"
            )
            send_telegram_message(msg)

if __name__ == "__main__":
    predict_and_notify()
