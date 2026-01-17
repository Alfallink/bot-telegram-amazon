import os
import random
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
AFFILIATE_LINK = os.getenv("SHOPEE_AFFILIATE_LINK")

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

KEYWORDS = [
    "fone bluetooth",
    "smartphone",
    "tablet",
    "smartwatch",
    "mouse",
    "teclado",
    "eletronicos"
]

def enviar_telegram(titulo, link, imagem, preco):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHAT_ID,
        "photo": imagem,
        "caption": (
            f"🔥 *OFERTA SHOPEE*\n\n"
            f"📦 {titulo}\n"
            f"💰 R$ {preco}\n\n"
            f"👉 [Comprar com desconto]({link})"
        ),
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

def buscar_produtos():
    keyword = random.choice(KEYWORDS)
    print("🔎 Palavra-chave:", keyword)

    params = {
        "by": "relevancy",
        "keyword": keyword,
        "limit": 20,
        "newest": 0,
        "order": "desc",
        "page_type": "search",
        "scenario": "PAGE_GLOBAL_SEARCH"
    }

    response = requests.get(
        "https://shopee.com.br/api/v4/search/search_items",
        headers=HEADERS,
        params=params,
        timeout=20
    )

    data = response.json()
    items = data.get("items", [])

    produtos = []

    for item in items:
        info = item.get("item_basic")
        if not info:
            continue

        titulo = info.get("name")
        preco = info.get("price") / 100000 if info.get("price") else None
        imagem = f"https://cf.shopee.com.br/file/{info.get('image')}"

        shop_id = info.get("shopid")
        item_id = info.get("itemid")

        if not shop_id or not item_id:
            continue

        link = f"{AFFILIATE_LINK}https://shopee.com.br/product/{shop_id}/{item_id}"

        produtos.append((titulo, link, imagem, preco))

        if len(produtos) >= 5:
            break

    return produtos

def main():
    print("🚀 Bot Shopee iniciado")

    produtos = buscar_produtos()

    if not produtos:
        print("⚠️ Nenhum produto encontrado")
        return

    for titulo, link, imagem, preco in produtos:
        enviar_telegram(titulo, link, imagem, preco)
        print("✅ Enviado:", titulo)

if __name__ == "__main__":
    main()
