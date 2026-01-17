import os
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
AFFILIATE_TAG = os.getenv("AMAZON_PARTNER_TAG")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

SEARCH_URLS = [
    "https://www.amazon.com.br/s?k=fone+bluetooth",
    "https://www.amazon.com.br/s?k=smartphone",
    "https://www.amazon.com.br/s?k=tablet",
    "https://www.amazon.com.br/s?k=smart+tv",
    "https://www.amazon.com.br/s?k=echo+dot",
    "https://www.amazon.com.br/s?k=teclado",
    "https://www.amazon.com.br/s?k=mouse",
    "https://www.amazon.com.br/s?k=gadgets+eletronicos"
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


def enviar_telegram(titulo, link, imagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHAT_ID,
        "photo": imagem,
        "caption": f"🔥 *ELETRÔNICO EM DESTAQUE*\n\n📦 {titulo}\n\n👉 [Ver na Amazon]({link})",
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)


def buscar_produtos():
    url = random.choice(SEARCH_URLS)
    print("🔎 Buscando em:", url)

    response = requests.get(url, headers=HEADERS, timeout=20)
    print("🌐 Status HTTP:", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    resultados = soup.select('div[data-component-type="s-search-result"]')
    print("📦 Resultados encontrados:", len(resultados))

    produtos = []

    for item in resultados:
        asin = item.get("data-asin")
        if not asin:
            continue

        titulo_tag = item.select_one("h2 span")
        link_tag = item.select_one("h2 a")
        img_tag = item.select_one("img")

        if not titulo_tag or not link_tag or not img_tag:
            continue

        titulo = titulo_tag.text.strip()
        href = link_tag.get("href")

        if not href.startswith("/"):
            continue

        link = f"https://www.amazon.com.br{href}&tag={AFFILIATE_TAG}"
        imagem = img_tag.get("src")

        if ja_enviado(link):
            continue

        produtos.append((titulo, link, imagem))

        if len(produtos) >= 5:
            break

    print("✅ Produtos válidos:", len(produtos))
    return produtos



def main():
    print("🚀 Bot iniciado")

    produtos = buscar_produtos()

    if not produtos:
        print("⚠️ Nenhum produto encontrado")
        return

    for titulo, link, imagem in produtos:
        enviar_telegram(titulo, link, imagem)
        marcar_enviado(link)
        print("✅ Enviado:", titulo)


if __name__ == "__main__":
    main()
