import os        
import random
import requests
from amazon_paapi import AmazonApi


ACCESS_KEY = os.getenv("AMAZON_ACCESS_KEY")
SECRET_KEY = os.getenv("AMAZON_SECRET_KEY")
PARTNER_TAG = os.getenv("AMAZON_PARTNER_TAG")


amazon = AmazonApi(
    ACCESS_KEY,
    SECRET_KEY,
    PARTNER_TAG,
    "BR"
)

KEYWORDS = [
    "fone de ouvido bluetooth",
    "smartphone",
    "tablet android",
    "smart tv",
    "echo dot alexa",
    "teclado mecanico",
    "mouse gamer",
    "gadget eletronico"
]

# ====== TELEGRAM CONFIG ======
TELEGRAM_URL = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_telegram(texto):
    requests.post(TELEGRAM_URL, json={
        "chat_id": CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    })

def buscar_produtos():
    keyword = random.choice(KEYWORDS)

    response = amazon.search_items(
        keywords=keyword,
        item_count=10
    )

    if not response or not response.items:
        return []

    return response.items


def main():
    produtos = buscar_produtos()
    enviados = 0

    for item in produtos:
        try:
            titulo = item.item_info.title.display_value
            preco = item.offers.listings[0].price.display_amount
            link = item.detail_page_url

            mensagem = f"""
🔥 *OFERTA ELETRÔNICA*

📦 *{titulo}*
💰 *{preco}*
🚀 Entrega Amazon

👉 [Comprar com desconto]({link})
"""
            enviar_telegram(mensagem)
            enviados += 1

            if enviados >= 5:
                break

        except Exception:
            continue

if __name__ == "__main__":
    main()
