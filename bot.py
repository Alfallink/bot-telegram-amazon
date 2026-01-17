import os
import random
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
AFFILIATE_LINK = os.getenv("SHOPEE_AFFILIATE_LINK")  # link base afiliado

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "pt-BR,pt;q=0.9"
}

SEARCH_URLS = [
    "https://shopee.com.br/search?keyword=fone%20bluetooth",
    "https://shopee.com.br/search?keyword=smartphone",
    "https://shopee.com.br/search?keyword=tablet",
    "https://shopee.com.br/search?keyword=smartwatch",
    "https://shopee.com.br/search?keyword=mouse",
    "https://shopee.com.br/search?keyword=teclado",
    "https://shopee.com.br/search?keyword=eletronicos"
]

ENVIADOS_FILE = "enviados.txt"


def ja_enviado(link):
    if not os.path.exists(ENVIADOS_FILE):
        return False
    with open(ENVIADOS_FILE, "r", encoding="utf-8") as f:
        return link in f.read()


def marcar_enviado(link):
    with open(ENVIADOS_FILE, "a", encoding="utf-8") as f:
        f.write(link + "\n")


def enviar_telegram(titulo, link, imagem, preco):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHAT_ID,
        "photo": imagem,
        "caption": (
            f"🔥 *OFERTA SHOPEE*\n\n"
            f"📦 {titulo}\n"
            f"💰 {preco}\n\n"
            f"👉 [Comprar com desconto]({link})"
        ),
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)


def buscar_produtos():
    url = random.choice(SEARCH_URLS)
    print("🔎 Buscando:", url)

    response = requests.get(url, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(response.text, "html.parser")

    produtos = []

    for item in soup.select("div.shopee-search-item-result__item"):
        link_tag = item.select_one("a")
        img_tag = item.select_one("img")
        titulo_tag = item.select_one("div._10Wbs-._5SSWfi.UjjMrh")
        preco_tag = item.select_one("span._29R_un")

        if not link_tag or not img_tag or not titulo_tag:
            continue

        link = "https://shopee.com.br" + link_tag.get("href")
        link_afiliado = AFFILIATE_LINK + link.split("?")[0]

        if ja_enviado(link_afiliado):
            continue

        imagem = img_tag.get("src")
        titulo = titulo_tag.text.strip()
        preco = preco_tag.text.strip() if preco_tag else "Confira no link"

        produtos.append((titulo, link_afiliado, imagem, preco))

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
        marcar_enviado(link)
        print("✅ Enviado:", titulo)


if __name__ == "__main__":
    main()
