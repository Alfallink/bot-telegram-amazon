import requests
from bs4 import BeautifulSoup
import os
import time
import random

# =========================
# SECRETS
# =========================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
AFILIADO_TAG = os.getenv("AFILIADO_TAG")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
}

# =========================
# CATEGORIAS
# =========================

CATEGORIAS = {
    "🔌 Eletrônicos": "https://www.amazon.com.br/gp/bestsellers/electronics",
    "🎮 Games & Videogame": "https://www.amazon.com.br/gp/bestsellers/videogames",
    "🎵 Música": "https://www.amazon.com.br/gp/bestsellers/music",
    "💻 Computadores": "https://www.amazon.com.br/gp/bestsellers/computers"
}

# =========================
# BUSCAR PRODUTOS
# =========================

def buscar_produtos(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    produtos = []

    itens = soup.select("div.zg-grid-general-faceout")
    random.shuffle(itens)

    for item in itens[:3]:
        titulo = item.select_one("div._cDEzb_p13n-sc-css-line-clamp-3_g3dy1")
        link = item.select_one("a.a-link-normal")

        if not titulo or not link:
            continue

        produtos.append({
            "titulo": titulo.get_text(strip=True),
            "link": "https://www.amazon.com.br" + link["href"].split("?")[0]
        })

    return produtos

# =========================
# ENVIAR TELEGRAM
# =========================

def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texto
    }
    requests.post(url, json=payload)

# =========================
# EXECUÇÃO
# =========================

print("🚀 Bot Loja Ponto H iniciado...")

categoria, url = random.choice(list(CATEGORIAS.items()))
produtos = buscar_produtos(url)

for p in produtos:
    link_afiliado = f"{p['link']}?tag={AFILIADO_TAG}"

🔥 OFERTA EM ALTA – LOJA PONTO H 🔥

📦 Produto que está entre os mais vendidos da Amazon
Ideal para quem busca qualidade e bom custo-benefício.

✅ Compra segura
✅ Entrega rápida
✅ Garantia Amazon

👉 Aproveite agora:
{LINK}

🏬 Loja Ponto H – Curadoria diária de tecnologia, games e eletrônicos.


    enviar_telegram(mensagem)
    time.sleep(3)

print("🏁 Execução finalizada.")
