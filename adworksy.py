import requests
import time
import json
from datetime import datetime
import threading
from flask import Flask

# ==== Flask dummy server ====
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Worker is running in background"

# ==== Original Script Config ====
URL = "https://shibaadearner.top/scratch/api/watch-ad.php"
USER_ID = 5531217637
REQUESTS_PER_HOUR = 15
DELAY_BETWEEN_REQUESTS = 60  # 1 minute in seconds

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Type': 'application/json',
    'Cookie': 'video_ad_watched=2025-09-28',
    'Origin': 'https://shibaadearner.top',
    'Referer': 'https://shibaadearner.top/scratch/',
    'Sec-Ch-Ua': '"Microsoft Edge";v="140", "Chromium";v="140", "Microsoft Edge WebView2";v="140", "Not=A?Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0'
}

payload = {
    "user_id": USER_ID
}

# ==== Functions ====
def send_request():
    try:
        response = requests.post(URL, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Success!")
            print(f"  Status: {data.get('status')}")
            print(f"  Message: {data.get('message')}")
            print(f"  New Balance: {data.get('new_balance')}")
            print(f"  Watches This Hour: {data.get('watches_this_hour')}")
            print(f"  Earned: {data.get('earned')}")
            print("-" * 50)
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Error: Status Code {response.status_code}")
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Request failed: {e}")

def worker_loop():
    print("Background worker started. Script will run continuously.")
    while True:
        start_time = time.time()
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting new hour cycle...")

        for i in range(REQUESTS_PER_HOUR):
            print(f"\nSending request {i+1}/{REQUESTS_PER_HOUR}")
            send_request()
            if i < REQUESTS_PER_HOUR - 1:
                print(f"Waiting {DELAY_BETWEEN_REQUESTS} seconds before next request...")
                time.sleep(DELAY_BETWEEN_REQUESTS)

        time_spent = time.time() - start_time
        remaining_time = 3600 - time_spent
        if remaining_time > 0:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Completed {REQUESTS_PER_HOUR} requests.")
            print(f"Waiting {int(remaining_time)} seconds ({remaining_time/60:.1f} minutes) until next hour...")
            time.sleep(remaining_time)

# ==== Entry point ====
if __name__ == "__main__":
    # Background thread
    t = threading.Thread(target=worker_loop)
    t.daemon = True
    t.start()

    # Flask server to keep Render happy
    app.run(host="0.0.0.0", port=10000)
