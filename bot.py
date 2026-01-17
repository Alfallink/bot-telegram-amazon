import os
import requests

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

resp = requests.post(url, json={
    "chat_id": CHAT_ID,
    
    def enviar_telegram(titulo, link, imagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "photo": imagem,
        "caption": f"🔥 *ELETRÔNICO EM DESTAQUE*\n\n📦 {titulo}\n\n👉 [Ver na Amazon]({link})",
        "parse_mode": "Markdown"
    })


print(resp.text)
