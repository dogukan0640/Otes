
import schedule, time, subprocess, os, sys, requests

TOKEN="7744478523:AAEtRJar6uF7m0cxKfQh7r7TltXYxWwtmm0"
CHAT="1009868232"
def tg(m): requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                         data={"chat_id":CHAT,"text":m})

def run(cmd): subprocess.run([sys.executable, cmd], check=True)

def ensure_model():
    if not os.path.exists("model.pkl"):
        run("train_model.py")
def analysis():
    try:
        run("data_collector.py")
        run("multi_timeframe_analysis.py")
        ensure_model()
        run("predictor.py")
    except Exception as e:
        tg(f"[HATA analysis] {e}")
def training():
    try: run("train_model.py")
    except Exception as e: tg(f"[HATA training] {e}")
def watcher():
    try: run("trade_result_watcher.py")
    except Exception as e: tg(f"[HATA watcher] {e}")

if __name__=="__main__":
    tg("[BOT] v2 başladı.")
    schedule.every(30).minutes.do(analysis)
    schedule.every(4).hours.do(training)
    schedule.every(5).minutes.do(watcher)
    while True:
        schedule.run_pending()
        time.sleep(1)
