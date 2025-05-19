import time
import schedule
import subprocess
import requests

TELEGRAM_TOKEN = "7744478523:AAEtRJar6uF7m0cxKfQh7r7TltXYxWwtmm0"
CHAT_ID = "1009868232"

def send_telegram_startup():
    msg = "[BOT BAŞLADI] AI analiz botu aktif. 30 dakikada bir tarama, 4 saatte bir eğitim yapacak."
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    requests.post(url, data=payload)

def run_analysis_cycle():
    try:
        subprocess.run(["python", "data_collector.py"], check=True)
        subprocess.run(["python", "multi_timeframe_analysis.py"], check=True)
        subprocess.run(["python", "predictor.py"], check=True)
    except Exception as e:
        error_msg = f"[HATA] Analiz döngüsünde hata: {str(e)}"
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": error_msg})

def run_training_cycle():
    try:
        subprocess.run(["python", "train_model.py"], check=True)
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": "[AI EĞİTİLDİ] Model yeniden eğitildi."})
    except Exception as e:
        error_msg = f"[HATA] Eğitim döngüsünde hata: {str(e)}"
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": error_msg})

if __name__ == "__main__":
    send_telegram_startup()
    schedule.every(30).minutes.do(run_analysis_cycle)
    schedule.every(4).hours.do(run_training_cycle)

    while True:
        schedule.run_pending()
        time.sleep(1)
