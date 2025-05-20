
import time, schedule, subprocess, requests, os, sys

TOKEN = "7744478523:AAEtRJar6uF7m0cxKfQh7r7TltXYxWwtmm0"
CHAT  = "1009868232"

def tg(msg):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                  data={"chat_id": CHAT, "text": msg})

def ensure_model():
    if not os.path.exists("model.pkl"):
        tg("[BOT] model.pkl bulunamadı, eğitim başlatılıyor...")
        subprocess.run([sys.executable,"train_model.py"],check=True)

def cycle_analysis():
    try:
        subprocess.run([sys.executable,"data_collector.py"],check=True)
        subprocess.run([sys.executable,"multi_timeframe_analysis.py"],check=True)
        ensure_model()
        subprocess.run([sys.executable,"predictor.py"],check=True)
    except Exception as e:
        tg(f"[HATA] analysis cycle\n{e}")

def cycle_training():
    try:
        subprocess.run([sys.executable,"train_model.py"],check=True)
        tg("[AI] Model yeniden eğitildi.")
    except Exception as e:
        tg(f"[HATA] training\n{e}")

def cycle_watcher():
    try:
        subprocess.run([sys.executable,"trade_result_watcher.py"],check=True)
    except Exception as e:
        tg(f"[HATA] watcher\n{e}")

if __name__=="__main__":
    tg("[BOT] Final AI bot başladı.")
    schedule.every(30).minutes.do(cycle_analysis)
    schedule.every(4).hours.do(cycle_training)
    schedule.every(5).minutes.do(cycle_watcher)
    while True:
        schedule.run_pending()
        time.sleep(1)
