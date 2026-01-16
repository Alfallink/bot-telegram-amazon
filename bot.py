import os
import time
import random
import requests

# =========================
# SECRETS (GITHUB ACTIONS)
# =========================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SHOPEE_AFILIADO_BASE = os.getenv("SHOPEE_AFILIADO_BASE")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN ausente")

if not TELEGRAM_CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID ausente")

if not SHOPEE_AFILIADO_BASE:
    raise ValueError("SHOPEE_AFILIADO_BASE ausente")

# =========================
# CONFIGURAÇÕES
# =========================

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://shopee.com.br/"
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
        "relogio inteligente"
    ],
    "🛡️ Capinhas e Películas": [
        "capinha celular",
        "pelicula vidro"
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
# TELEGRAM
# =========================

def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texto
    }

    r = requests.post(url, json=payload, timeout=10)
    print("📡 Telegram status:", r.status_code)

# =========================
# GERAR LINK AFILIADO
# =========================

def gerar_link_afiliado(link_produto):
    return f"{SHOPEE_AFILIADO_BASE}?u={link_produto}"

# =========================
# BUSCAR PRODUTOS SHOPEE (JSON)
# =========================

def buscar_produtos(palavra_chave, limite=1):
    print(f"🌐 Buscando na Shopee: {palavra_chave}")

    url = "https://shopee.com.br/api/v4/search/search_items"

    params = {
        "by": "relevancy",
        "keyword": palavra_chave,
        "limit": limite,
        "newest": 0,
        "order": "desc",
        "page_type": "search"
    }

    try:
        r = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=8  # evita travamento
        )

        if r.status_code != 200:
            print("⚠️ Shopee status:", r.status_code)
            return []

        data = r.json()

    except requests.exceptions.Timeout:
        print("⏱️ Timeout Shopee")
        return []

    except Exception as e:
        print("❌ Erro Shopee:", e)
        return []

    produtos = []

    for item in data.get("items", []):
        info = item.get("item_basic", {})

        titulo = info.get("name")
        shopid = info.get("shopid")
        itemid = info.get("itemid")

        if not titulo or not shopid or not itemid:
            continue

        link_produto = f"https://shopee.com.br/product/{shopid}/{itemid}"
        link_afiliado = gerar_link_afiliado(link_produto)

        produtos.append({
            "titulo": titulo,
            "link": link_afiliado
        })

        if len(produtos) >= limite:
            break

    return produtos

# =========================
# COPY PROFISSIONAL
# =========================

def gerar_mensagem(categoria, titulo, link):
    return f"""🔥 OFERTA EM ALTA – LOJA PONTO H 🔥

📂 Categoria: {categoria}

📦 {titulo}

✔️ Alta procura
✔️ Excelente custo-benefício
✔️ Compra segura pela Shopee

🛒 Garanta o seu agora:
{link}

🏬 Loja Ponto H
Tecnologia e eletrônicos selecionados.
"""

# =========================
# EXECUÇÃO PRINCIPAL
# =========================

print("🚀 Bot Shopee Loja Ponto H iniciado")

QTDE_POR_EXECUCAO = random.randint(3, 5)
print("📦 Quantidade desta execução:", QTDE_POR_EXECUCAO)

for i in range(QTDE_POR_EXECUCAO):
    categoria = random.choice(list(CATEGORIAS.keys()))
    palavra = random.choice(CATEGORIAS[categoria])

    print(f"🔎 ({i+1}/{QTDE_POR_EXECUCAO}) Categoria: {categoria} | Palavra: {palavra}")

    produtos = buscar_produtos(palavra, limite=1)

    if not produtos:
        print("⚠️ Nenhum produto retornado, pulando")
        continue

    for p in produtos:
        mensagem = gerar_mensagem(categoria, p["titulo"], p["link"])
        enviar_telegram(mensagem)

    # ⏳ intervalo curto (estável para GitHub)
    if i < QTDE_POR_EXECUCAO - 1:
        time.sleep(15)

print("🏁 Execução finalizada com sucesso")

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
