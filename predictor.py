import pandas as pd
import joblib
import requests
import numpy as np
import traceback

MODEL_PATH = "model.pkl"
TELEGRAM_TOKEN = "7744478523:AAEtRJar6uF7m0cxKfQh7r7TltXYxWwtmm0"
CHAT_ID = "1009868232"

def send_telegram_message(message: str) -> None:
    """Send a plain‑text message to Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

def predict_and_notify() -> None:
    """Load model & enriched signals, send strong‑confidence alerts."""
    try:
        model = joblib.load(MODEL_PATH)
        df = pd.read_csv("signals_enriched.csv").dropna()

        features = ["rsi", "atr"]
        X = df[features]
        df["ai_confidence"] = model.predict_proba(X)[:, 1] * 100   # 0‑1 → %

        strong = df[df["ai_confidence"] >= 70]

        if strong.empty:
            send_telegram_message("[BOT] Güçlü bir sinyal bulunamadı.")
            return

        for _, row in strong.iterrows():
            msg = (
                f"[AI Sinyal] {row['symbol']} - {row['interval']}\n"
                f"RSI: {row['rsi']:.2f} | ATR: {row['atr']:.2f}\n"
                f"Trend: {row['trend_direction']}\n"
                f"Entry: {row['entry_price']}  TP: {row['tp']}  SL: {row['sl']}\n"
                f"AI Güven: {row['ai_confidence']:.2f}%"
            )
            send_telegram_message(msg)

    except Exception:
        send_telegram_message(f"[HATA] predictor.py\n{traceback.format_exc()}")
        raise

if __name__ == "__main__":
    predict_and_notify()
