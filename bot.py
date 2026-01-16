import os
import random
import time
import requests
from amazon_paapi import AmazonApi

# =========================
# AMAZON PA-API
# =========================

AMAZON_ACCESS_KEY = os.getenv("AMAZON_ACCESS_KEY")
AMAZON_SECRET_KEY = os.getenv("AMAZON_SECRET_KEY")
AMAZON_PARTNER_TAG = os.getenv("AMAZON_PARTNER_TAG")
AMAZON_COUNTRY = "BR"

amazon = AmazonApi(
    AMAZON_ACCESS_KEY,
    AMAZON_SECRET_KEY,
    AMAZON_PARTNER_TAG,
    AMAZON_COUNTRY
)

# =========================
# TELEGRAM
# =========================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "disable_web_page_preview": False
    }
    r = requests.post(url, json=payload, timeout=20)
    print("📡 Telegram:", r.status_code)

# =========================
# PALAVRAS-CHAVE (ELETRÔNICOS TOP)
# =========================

KEYWORDS = [
    "smartphone",
    "iphone",
    "celular android",
    "tablet",
    "smart tv",
    "televisão 4k",
    "echo dot",
    "alexa",
    "fone bluetooth",
    "headphone",
    "smartwatch",
    "monitor gamer",
    "notebook",
    "mouse gamer",
    "teclado mecanico",
    "capinha celular",
    "pelicula vidro"
]

# =========================
# COPY AGRESSIVA
# =========================

def gerar_mensagem(categoria, titulo, link):
    return f"""🔥 OFERTA IMPERDÍVEL – LOJA PONTO H 🔥

📂 Categoria: {categoria}

📦 {titulo}

⚡ Alta procura
💎 Produto premium
🚚 Entrega rápida Amazon
🔒 Compra 100% segura

🛒 Garanta o seu agora:
{link}

🏬 Loja Ponto H
Os eletrônicos mais desejados do momento.
"""

# =========================
# BUSCAR PRODUTOS
# =========================

def buscar_produtos():
    palavra = random.choice(KEYWORDS)

    resultado = amazon.search_items(
        keywords=palavra,
        search_index="Electronics",
        item_count=random.randint(3, 6),
        resources=[
            "ItemInfo.Title",
            "DetailPageURL"
        ]
    )

    if not resultado or not resultado.items:
        return []

    produtos = []
    for item in resultado.items:
        try:
            produtos.append({
                "titulo": item.item_info.title.display_value,
                "link": item.detail_page_url
            })
        except:
            pass

    return produtos

# =========================
# EXECUÇÃO PRINCIPAL
# =========================

print("🚀 Bot Loja Ponto H iniciado")

produtos = buscar_produtos()
print("📦 Produtos encontrados:", len(produtos))

for p in produtos:
    mensagem = gerar_mensagem("Eletrônicos Premium", p["titulo"], p["link"])
    enviar_telegram(mensagem)

    # ⏳ Intervalo humano (2 a 6 minutos)
    time.sleep(random.randint(120, 360))

print("🏁 Execução finalizada")
