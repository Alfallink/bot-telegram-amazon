import os
import requests

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

resp = requests.post(url, json={
    "chat_id": CHAT_ID,
    "text": "✅ Teste OK: GitHub → Telegram funcionando"
})

print(resp.text)
