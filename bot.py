import requests
import os
import time
import random
from bs4 import BeautifulSoup

# =========================
# SECRETS
# =========================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SHOPEE_AFILIADO_BASE = os.getenv("SHOPEE_AFILIADO_BASE")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID or not SHOPEE_AFILIADO_BASE:
    raise ValueError("Secrets obrigatórios não definidos")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# =========================
# CATEGORIAS + PALAVRAS-CHAVE
# =========================

CATEGORIAS = {
    "📱 Celulares": [
        "iphone",
        "samsung galaxy",
        "xiaomi celular",
        "motorola celular"
    ],
    "📺 Televisões": [
        "smart tv",
        "tv 4k",
        "android tv"
    ],
    "🎧 Fones de Ouvido": [
        "fone bluetooth",
        "headphone",
        "fone gamer"
    ],
    "⌚ Smartwatch": [
        "smartwatch",
        "relógio inteligente"
    ],
    "🛡️ Capinhas e Películas": [
        "capinha celular",
        "película vidro"
    ],
    "🔊 Assistentes Virtuais": [
        "echo dot",
        "alexa"
    ],
    "💻 Eletrônicos em Geral": [
        "tablet",
        "monitor",
        "notebook"
    ]
}

# =========================
# GERAR LINK AFILIADO
# =========================

def gerar_link_afiliado(link_produto):
    return f"{SHOPEE_AFILIADO_BASE}?u={link_produto}"

# =========================
# BUSCAR PRODUTOS SHOPEE
# =========================

def buscar_produtos(palavra_chave, limite=1):
    url = "https://shopee.com.br/api/v4/search/search_items"

    params = {
        "by": "relevancy",
        "keyword": palavra_chave,
        "limit": limite,
        "newest": 0,
        "order": "desc",
        "page_type": "search"
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://shopee.com.br/"
    }

    r = requests.get(url, params=params, headers=headers, timeout=20)
    data = r.json()

    produtos = []

    for item in data.get("items", []):
        info = item.get("item_basic", {})

        titulo = info.get("name")
        shopid = info.get("shopid")
        itemid = info.get("itemid")

        if not titulo or not shopid or not itemid:
            continue

        link_produto = f"https://shopee.com.br/product/{shopid}/{itemid}"
        link_afiliado = f"{SHOPEE_AFILIADO_BASE}?u={link_produto}"

        produtos.append({
            "titulo": titulo,
            "link": link_afiliado
        })

        if len(produtos) >= limite:
            break

    return produtos

# =========================
# TELEGRAM
# =========================

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg
    })

# =========================
# COPY AGRESSIVA
# =========================

def gerar_mensagem(categoria, titulo, link):
    return f"""🔥 OFERTA IMPERDÍVEL – LOJA PONTO H 🔥

📂 Categoria: {categoria}

📦 {titulo}

⚡ Alta procura
💎 Excelente custo-benefício
🚚 Envio rápido Shopee
🔒 Compra segura

🛒 Garanta o seu agora:
{link}

🏬 Loja Ponto H
Os eletrônicos mais desejados do momento.
"""

# =========================
# EXECUÇÃO PRINCIPAL
# =========================

print("🚀 Bot Shopee Loja Ponto H iniciado")

QTDE_POR_EXECUCAO = random.randint(3, 6)

for i in range(QTDE_POR_EXECUCAO):
    categoria = random.choice(list(CATEGORIAS.keys()))
    palavra = random.choice(CATEGORIAS[categoria])

    print(f"🔎 Buscando: {categoria} | {palavra}")

    produtos = buscar_produtos(palavra, limite=1)

    for p in produtos:
        mensagem = gerar_mensagem(categoria, p["titulo"], p["link"])
        enviar_telegram(mensagem)

    if i < QTDE_POR_EXECUCAO - 1:
        time.sleep(random.randint(120, 360))  # 2 a 6 minutos

print("🏁 Execução finalizada")
