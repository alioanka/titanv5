# telegram/bot.py

import requests
from config import TELEGRAM_ENABLED, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def send_alert(message: str):
    if not TELEGRAM_ENABLED:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        requests.post(url, json=payload)
    except Exception as e:
        print(f"❌ Failed to send Telegram alert: {e}")
