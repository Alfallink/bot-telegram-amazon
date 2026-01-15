# ==========================================
# BOT TELEGRAM AMAZON AFILIADO
# AUTOMÁTICO PELO GITHUB
# ==========================================

import requests
from bs4 import BeautifulSoup
import time
import random
import os

# ==========================================
# VARIÁVEIS (VÊM DOS SECRETS DO GITHUB)
# ==========================================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
AFILIADO_TAG = os.getenv("AFILIADO_TAG")

# ==========================================
# LISTA DE PRODUTOS (ASINS)
# você pode trocar depois
# ==========================================

ASINS = [
    "B09ZV5KZ2Z",
    "B0C5B8Z4ZP",
    "B07FZ8S74R"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
}

# ==========================================
# BUSCAR DADOS DO PRODUTO NA AMAZON
# ==========================================

def buscar_produto(asin):
    url = f"https://www.amazon.com.br/dp/{asin}"
    r = requests.get(url, headers=HEADERS, timeout=20)

    if r.status_code != 200:
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    titulo = soup.select_one("#productTitle")
    titulo = titulo.get_text(strip=True) if titulo else "Produto Amazon"

    preco = soup.select_one(".a-offscreen")
    preco = preco.get_text(strip=True) if preco else "Confira no link"

    img = soup.select_one("#landingImage")
    imagem = img["src"] if img else None

    return {
        "titulo": titulo,
        "preco": preco,
        "imagem": imagem,
        "link": f"https://www.amazon.com.br/dp/{asin}?tag={AFILIADO_TAG}"
    }

# ==========================================
# TEXTO DA MENSAGEM
# ==========================================

def criar_legenda(p):
    chamadas = [
        "🔥 OFERTA NA AMAZON 🔥",
        "⚡ PREÇO BAIXO AGORA ⚡",
        "💥 PROMOÇÃO IMPERDÍVEL 💥"
    ]

    return f"""{random.choice(chamadas)}

📦 <b>{p['titulo']}</b>
💰 <b>Preço:</b> {p['preco']}

👉 <a href="{p['link']}">COMPRAR AGORA</a>
"""

# ==========================================
# ENVIAR PARA TELEGRAM
# ==========================================

def enviar_telegram(produto):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "photo": produto["imagem"],
        "caption": criar_legenda(produto),
        "parse_mode": "HTML"
    }

    return requests.post(url, data=payload).status_code

# ==========================================
# EXECUÇÃO
# ==========================================

print("🚀 Bot iniciado...")

for asin in ASINS:
    produto = buscar_produto(asin)

    if not produto or not produto["imagem"]:
        print("❌ Erro no ASIN:", asin)
        continue

    status = enviar_telegram(produto)
    print("✅ Enviado:", produto["titulo"], "| Status:", status)

    time.sleep(5)  # evita bloqueio

print("🏁 Finalizado.")
