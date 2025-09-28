import requests
import time
import json
from datetime import datetime

# Configuration
URL = "https://shibaadearner.top/scratch/api/watch-ad.php"
USER_ID = 5531217637
REQUESTS_PER_HOUR = 15
DELAY_BETWEEN_REQUESTS = 60  # 1 minute in seconds

# Headers
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

# Payload
payload = {
    "user_id": USER_ID
}

def send_request():
    """Send a single request and return the response"""
    try:
        response = requests.post(URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Success!")
            print(f"  Status: {data.get('status')}")
            print(f"  Message: {data.get('message')}")
            print(f"  New Balance: {data.get('new_balance')}")
            print(f"  Watches This Hour: {data.get('watches_this_hour')}")
            print(f"  Earned: {data.get('earned')}")
            print("-" * 50)
            return True
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error: Status Code {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Request failed: {e}")
        return False
    except json.JSONDecodeError:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Failed to parse response")
        return False

def main():
    """Main function to run the script continuously"""
    print("Script started. Press Ctrl+C to stop.")
    print("=" * 50)
    
    while True:
        start_time = time.time()
        
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting new hour cycle...")
        
        # Send 15 requests with 1 minute delay between each
        for i in range(REQUESTS_PER_HOUR):
            print(f"\nSending request {i+1}/{REQUESTS_PER_HOUR}")
            send_request()
            
            # Wait 1 minute before next request (except after the last request)
            if i < REQUESTS_PER_HOUR - 1:
                print(f"Waiting {DELAY_BETWEEN_REQUESTS} seconds before next request...")
                time.sleep(DELAY_BETWEEN_REQUESTS)
        
        # Calculate time spent and remaining time in the hour
        time_spent = time.time() - start_time
        remaining_time = 3600 - time_spent  # 3600 seconds = 1 hour
        
        if remaining_time > 0:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Completed {REQUESTS_PER_HOUR} requests.")
            print(f"Waiting {int(remaining_time)} seconds ({remaining_time/60:.1f} minutes) until next hour...")
            time.sleep(remaining_time)
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScript stopped by user.")