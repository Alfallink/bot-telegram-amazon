import os
import random
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
AFFILIATE_TAG = os.getenv("AMAZON_PARTNER_TAG")

SEARCH_URLS = [
    "https://www.amazon.com.br/s?k=fone+bluetooth",
    "https://www.amazon.com.br/s?k=smartphone",
    "https://www.amazon.com.br/s?k=tablet",
    "https://www.amazon.com.br/s?k=smart+tv",
    "https://www.amazon.com.br/s?k=echo+dot",
    "https://www.amazon.com.br/s?k=teclado+usb",
    "https://www.amazon.com.br/s?k=mouse+usb"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    })

def buscar_produtos():
    url = random.choice(SEARCH_URLS)
    html = requests.get(url, headers=HEADERS).text
    soup = BeautifulSoup(html, "html.parser")

    produtos = []
    for item in soup.select("div.s-result-item"):
        link = item.select_one("a.a-link-normal")
        titulo = item.select_one("span.a-text-normal")

        if link and titulo:
            href = "https://www.amazon.com.br" + link.get("href")
            afiliado = f"{href}&tag={AFFILIATE_TAG}"
            produtos.append((titulo.text.strip(), afiliado))

        if len(produtos) >= 5:
            break

    return produtos

def main():
    produtos = buscar_produtos()
    for titulo, link in produtos:
        mensagem = f"""
🔥 *ELETRÔNICO EM DESTAQUE*

📦 {titulo}

👉 [Ver na Amazon]({link})
"""
        enviar_telegram(mensagem)

if __name__ == "__main__":
    main()
