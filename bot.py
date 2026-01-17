import os
import time
import hmac
import hashlib
import requests
import json

PARTNER_ID = int(os.getenv("SHOPEE_PARTNER_ID"))
PARTNER_KEY = os.getenv("SHOPEE_PARTNER_KEY")
PARTNER_SECRET = os.getenv("SHOPEE_PARTNER_SECRET")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

BASE_URL = "https://partner.shopeemobile.com"
PATH = "/api/v2/product/search_item"

def generate_signature(path, timestamp):
    base_string = f"{PARTNER_ID}{path}{timestamp}"
    return hmac.new(
        PARTNER_SECRET.encode(),
        base_string.encode(),
        hashlib.sha256
    ).hexdigest()

def shopee_request():
    timestamp = int(time.time())
    sign = generate_signature(PATH, timestamp)

    params = {
        "partner_id": PARTNER_ID,
        "timestamp": timestamp,
        "sign": sign,
        "page_size": 5
    }

    url = BASE_URL + PATH
    response = requests.get(url, params=params, timeout=20)
    return response.json()

def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown"
    })

def main():
    print("🚀 Bot Shopee API iniciado")

    data = shopee_request()
    items = data.get("items", [])

    if not items:
        print("⚠️ Nenhum produto retornado pela API")
        return

    for item in items:
        nome = item.get("item_name")
        preco = item.get("price_info", {}).get("price")
        link = item.get("item_link")

        mensagem = f"""
🔥 *OFERTA SHOPEE*

📦 {nome}
💰 {preco}

👉 Comprar:
{link}
"""
        enviar_telegram(mensagem)
        print("✅ Enviado:", nome)

if __name__ == "__main__":
    main()
