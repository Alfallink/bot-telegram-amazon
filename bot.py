import requests
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

resp = requests.post(
    URL,
    json={
        "chat_id": CHAT_ID,
        "text": "✅ Bot rodando corretamente",
        "parse_mode": "Markdown"
    }
)

print(resp.text)
